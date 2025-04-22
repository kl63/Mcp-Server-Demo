from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List, Any
import requests
import base64
import json
import os
from urllib.parse import urlparse

# Create the MCP server
mcp = FastMCP("GitHub Code Review MCP")

# Store for repository data and review information
repo_data = {}


@mcp.tool()
def review_repository(repo_url: str, focus_areas: Optional[str] = None) -> Dict[str, Any]:
    """
    Review a GitHub repository using Claude
    
    Args:
        repo_url: URL of the GitHub repository to review (e.g., https://github.com/username/repo)
        focus_areas: Optional specific areas to focus the review on (e.g., "security, performance, best practices")
    
    Returns:
        A dictionary containing the review results
    """
    # Parse repository information from URL
    parsed_url = urlparse(repo_url)
    
    if "github.com" not in parsed_url.netloc:
        return {"error": "Invalid GitHub URL. Please provide a valid GitHub repository URL."}
    
    # Extract username and repo name from path
    path_parts = [p for p in parsed_url.path.split('/') if p]
    if len(path_parts) < 2:
        return {"error": "Invalid GitHub repository URL format."}
    
    owner = path_parts[0]
    repo = path_parts[1]
    
    # Get repository data
    repo_info = fetch_repo_info(owner, repo)
    if "error" in repo_info:
        return repo_info
    
    # Get repository files
    files = fetch_repo_files(owner, repo)
    if "error" in files:
        return files
    
    # Prepare code for review
    code_content = prepare_code_for_review(files)
    
    # Create review prompt based on focus areas
    review_prompt = create_review_prompt(code_content, focus_areas)
    
    # Generate review using Claude (in a real implementation, this would call Claude API)
    review_results = generate_review(review_prompt)
    
    # Store the results for this repository
    repo_key = f"{owner}/{repo}"
    repo_data[repo_key] = {
        "repo_info": repo_info,
        "review_results": review_results,
        "focus_areas": focus_areas
    }
    
    return {
        "repo": repo_key,
        "review": review_results,
        "status": "completed"
    }


@mcp.tool()
def list_reviewed_repos() -> List[Dict[str, Any]]:
    """
    List all repositories that have been reviewed
    
    Returns:
        A list of repository information with review statuses
    """
    result = []
    for repo_key, data in repo_data.items():
        result.append({
            "repo": repo_key,
            "review_date": data.get("review_date", "N/A"),
            "focus_areas": data.get("focus_areas", "General review")
        })
    return result


@mcp.tool()
def get_review_details(repo_key: str) -> Dict[str, Any]:
    """
    Get detailed review results for a specific repository
    
    Args:
        repo_key: Repository key in the format "owner/repo"
    
    Returns:
        Detailed review information for the specified repository
    """
    if repo_key not in repo_data:
        return {"error": "Repository review not found."}
    
    return repo_data[repo_key]


@mcp.tool()
def suggest_improvements(repo_key: str, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Suggest specific improvements for a repository or file
    
    Args:
        repo_key: Repository key in the format "owner/repo"
        file_path: Optional path to specific file for focused suggestions
    
    Returns:
        Improvement suggestions for the repository or file
    """
    if repo_key not in repo_data:
        return {"error": "Repository review not found."}
    
    # In a real implementation, this would call Claude with specific prompts
    # for generating improvement suggestions
    
    repository_data = repo_data[repo_key]
    code_content = repository_data.get("code_content", {})
    
    if file_path and file_path in code_content:
        # Generate suggestions for specific file
        file_content = code_content[file_path]
        suggestions = generate_file_suggestions(file_content, file_path)
        return {
            "repo": repo_key,
            "file": file_path,
            "suggestions": suggestions
        }
    else:
        # Generate suggestions for entire repository
        suggestions = generate_repo_suggestions(repository_data)
        return {
            "repo": repo_key,
            "suggestions": suggestions
        }


# Helper functions
def fetch_repo_info(owner: str, repo: str) -> Dict[str, Any]:
    """Fetch repository information from GitHub API"""
    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch repository information: {response.status_code}"}
    except Exception as e:
        return {"error": f"Error fetching repository information: {str(e)}"}


def fetch_repo_files(owner: str, repo: str, path: str = "") -> Dict[str, Any]:
    """Fetch repository files from GitHub API"""
    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}")
        if response.status_code != 200:
            return {"error": f"Failed to fetch repository contents: {response.status_code}"}
        
        contents = response.json()
        result = {}
        
        if isinstance(contents, list):
            for item in contents:
                if item["type"] == "file":
                    # Get file content
                    file_content = fetch_file_content(owner, repo, item["path"])
                    if "error" not in file_content:
                        result[item["path"]] = file_content
                elif item["type"] == "dir":
                    # Recursively fetch directory contents
                    sub_contents = fetch_repo_files(owner, repo, item["path"])
                    if "error" not in sub_contents:
                        result.update(sub_contents)
        
        return result
    except Exception as e:
        return {"error": f"Error fetching repository files: {str(e)}"}


def fetch_file_content(owner: str, repo: str, path: str) -> Dict[str, Any]:
    """Fetch content of a specific file from GitHub API"""
    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}")
        if response.status_code == 200:
            content_data = response.json()
            if content_data.get("encoding") == "base64" and content_data.get("content"):
                return {
                    "content": base64.b64decode(content_data["content"]).decode("utf-8"),
                    "path": path,
                    "size": content_data.get("size", 0)
                }
        return {"error": f"Failed to fetch file content: {response.status_code}"}
    except Exception as e:
        return {"error": f"Error fetching file content: {str(e)}"}


def prepare_code_for_review(files: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare code content for review"""
    processed_files = {}
    for path, file_data in files.items():
        # Skip binary files, large files, etc.
        if isinstance(file_data, dict) and "content" in file_data:
            # Filter to only include code files
            if is_code_file(path):
                processed_files[path] = file_data
    
    return processed_files


def is_code_file(path: str) -> bool:
    """Check if a file is a code file based on extension"""
    code_extensions = [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".cs", 
        ".go", ".rb", ".php", ".swift", ".kt", ".rs", ".html", ".css", ".scss"
    ]
    return any(path.endswith(ext) for ext in code_extensions)


def create_review_prompt(code_content: Dict[str, Any], focus_areas: Optional[str] = None) -> str:
    """Create a prompt for Claude to review the code"""
    prompt = "Please review the following code repository:\n\n"
    
    # Add focus areas to prompt if specified
    if focus_areas:
        prompt += f"Focus areas for review: {focus_areas}\n\n"
    else:
        prompt += "Please provide a general code review covering best practices, potential bugs, and performance issues.\n\n"
    
    # Add code files to prompt
    for path, file_data in code_content.items():
        prompt += f"File: {path}\n"
        prompt += "```\n"
        prompt += file_data.get("content", "")
        prompt += "\n```\n\n"
    
    return prompt


def generate_review(prompt: str) -> Dict[str, Any]:
    """
    Generate a code review using Claude API
    
    In a real implementation, this would call Claude's API
    For this demo, we'll return a placeholder response
    """
    # In a real implementation, you'd send the prompt to Claude API
    # and get back a detailed code review
    
    # This is where you would make the actual call to Claude
    # Placeholder for demonstration
    return {
        "summary": "Code review generated successfully",
        "details": "This is a placeholder for the actual code review that would be generated by Claude."
    }


def generate_file_suggestions(file_content: Dict[str, Any], file_path: str) -> List[Dict[str, Any]]:
    """Generate improvement suggestions for a specific file"""
    # In a real implementation, this would call Claude with a specific prompt
    # for generating file-level improvement suggestions
    
    # Placeholder for demonstration
    return [
        {
            "line": 10,
            "suggestion": "Consider using a more descriptive variable name",
            "severity": "low"
        }
    ]


def generate_repo_suggestions(repo_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate improvement suggestions for an entire repository"""
    # In a real implementation, this would call Claude with a specific prompt
    # for generating repository-level improvement suggestions
    
    # Placeholder for demonstration
    return {
        "architecture": [
            "Consider implementing a more modular file structure"
        ],
        "best_practices": [
            "Add comprehensive unit tests for core functionality",
            "Implement proper error handling throughout the codebase"
        ],
        "performance": [
            "Optimize database queries in the user service"
        ]
    }
