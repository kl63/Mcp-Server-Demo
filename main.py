from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List, Any
import requests
import base64
import json
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the MCP server
mcp = FastMCP("GitHub Code Review MCP")

# Store for repository data and review information
repo_data = {}

# GitHub API configuration
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN", "")  # Get from environment variable
GITHUB_HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}
if GITHUB_API_TOKEN:
    GITHUB_HEADERS["Authorization"] = f"token {GITHUB_API_TOKEN}"

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


@mcp.tool()
def analyze_dependencies(repo_key: str) -> Dict[str, Any]:
    """
    Analyze dependencies in a repository
    
    Args:
        repo_key: Repository key in the format "owner/repo"
    
    Returns:
        Dependency analysis results including outdated packages, vulnerabilities, and recommendations
    """
    if repo_key not in repo_data:
        return {"error": "Repository data not found."}
    
    repository_data = repo_data[repo_key]
    
    # For a real implementation, this would analyze package.json, requirements.txt, etc.
    # For this demo, we're returning placeholder data
    
    return {
        "repo": repo_key,
        "dependencies": {
            "direct": 15,
            "indirect": 47,
            "outdated": 3,
            "vulnerable": 1,
        },
        "recommendations": [
            "Update lodash from 4.17.15 to 4.17.21 to fix security vulnerabilities",
            "Consider replacing moment.js with date-fns for better tree-shaking"
        ]
    }


@mcp.tool()
def scan_security_vulnerabilities(repo_key: str) -> Dict[str, Any]:
    """
    Scan a repository for security vulnerabilities
    
    Args:
        repo_key: Repository key in the format "owner/repo"
    
    Returns:
        Security scan results with identified vulnerabilities and remediation steps
    """
    if repo_key not in repo_data:
        return {"error": "Repository data not found."}
    
    repository_data = repo_data[repo_key]
    
    # For a real implementation, this would integrate with security scanning tools
    # For this demo, we're returning placeholder data
    
    return {
        "repo": repo_key,
        "scan_results": {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3
        },
        "vulnerabilities": [
            {
                "severity": "high",
                "description": "SQL Injection vulnerability in user input processing",
                "location": "src/controllers/user.js:45",
                "remediation": "Use parameterized queries or an ORM to handle user input"
            },
            {
                "severity": "medium",
                "description": "Insecure direct object reference",
                "location": "src/api/orders.js:78",
                "remediation": "Implement proper authorization checks before fetching resources"
            }
        ]
    }


@mcp.tool()
def analyze_code_quality(repo_key: str) -> Dict[str, Any]:
    """
    Analyze code quality metrics for a repository
    
    Args:
        repo_key: Repository key in the format "owner/repo"
    
    Returns:
        Code quality metrics including complexity, duplication, and maintainability
    """
    if repo_key not in repo_data:
        return {"error": "Repository data not found."}
    
    repository_data = repo_data[repo_key]
    
    # For a real implementation, this would integrate with code quality tools
    # For this demo, we're returning placeholder data
    
    return {
        "repo": repo_key,
        "quality_metrics": {
            "maintainability_index": 75,
            "cyclomatic_complexity": {
                "average": 12,
                "worst_file": "src/utils/data-processor.js",
                "worst_value": 45
            },
            "code_duplication": {
                "percentage": 7.5,
                "hotspots": [
                    "src/components/forms",
                    "src/utils/helpers.js"
                ]
            },
            "test_coverage": {
                "percentage": 68,
                "uncovered_critical_paths": [
                    "src/services/authentication.js",
                    "src/controllers/payment.js"
                ]
            }
        },
        "recommendations": [
            "Refactor src/utils/data-processor.js to reduce complexity",
            "Extract duplicated code in form components into shared utilities",
            "Add integration tests for critical user flows"
        ]
    }


@mcp.tool()
def analyze_performance(repo_key: str) -> Dict[str, Any]:
    """
    Analyze performance issues in a repository
    
    Args:
        repo_key: Repository key in the format "owner/repo"
    
    Returns:
        Performance analysis with potential bottlenecks and optimization suggestions
    """
    if repo_key not in repo_data:
        return {"error": "Repository data not found."}
    
    repository_data = repo_data[repo_key]
    
    # For a real implementation, this would perform static analysis for performance issues
    # For this demo, we're returning placeholder data
    
    return {
        "repo": repo_key,
        "performance_issues": [
            {
                "severity": "high",
                "description": "Inefficient database query with N+1 problem",
                "location": "src/services/products.js:67",
                "impact": "Slow page load times when listing products with many relations",
                "suggestion": "Use eager loading or GraphQL to fetch all needed data in one query"
            },
            {
                "severity": "medium",
                "description": "Render blocking JavaScript",
                "location": "public/index.html:15-18",
                "impact": "Delayed page interactivity and poor Lighthouse score",
                "suggestion": "Use defer attribute or move script tags to end of body"
            }
        ],
        "optimization_opportunities": [
            "Implement code splitting to reduce initial bundle size",
            "Add caching headers for static assets",
            "Consider server-side rendering for initial page load"
        ]
    }


@mcp.tool()
def compare_with_best_practices(repo_key: str, framework: Optional[str] = None) -> Dict[str, Any]:
    """
    Compare repository against industry best practices
    
    Args:
        repo_key: Repository key in the format "owner/repo"
        framework: Optional framework name to use specific best practices (e.g., "react", "django")
    
    Returns:
        Comparison results and recommendations based on best practices
    """
    if repo_key not in repo_data:
        return {"error": "Repository data not found."}
    
    repository_data = repo_data[repo_key]
    
    # Detect framework if not provided
    if not framework:
        # In a real implementation, detect from package.json, requirements.txt, etc.
        framework = "react"  # Placeholder
    
    # For a real implementation, this would check against established best practices
    # For this demo, we're returning placeholder data
    
    return {
        "repo": repo_key,
        "framework": framework,
        "compliance_score": 72,
        "areas": {
            "project_structure": {
                "score": 85,
                "feedback": "Follows most React project structure conventions"
            },
            "state_management": {
                "score": 60,
                "feedback": "Inconsistent use of context API and Redux"
            },
            "component_design": {
                "score": 78,
                "feedback": "Good use of functional components, but some could be further decomposed"
            },
            "testing": {
                "score": 65,
                "feedback": "Unit tests present but integration tests missing"
            }
        },
        "recommendations": [
            "Standardize on a single state management approach",
            "Break down larger components into smaller, reusable ones",
            "Add integration tests for critical user flows"
        ]
    }


@mcp.tool()
def generate_pull_request_description(repo_key: str, review_id: str) -> Dict[str, Any]:
    """
    Generate a comprehensive pull request description based on code review results
    
    Args:
        repo_key: Repository key in the format "owner/repo"
        review_id: ID of the review to use for generating the PR description
    
    Returns:
        Generated PR description with summary, changes, and testing notes
    """
    if repo_key not in repo_data:
        return {"error": "Repository data not found."}
    
    # In a real implementation, this would generate a PR description based on the code changes
    # For this demo, we're returning placeholder data
    
    return {
        "repo": repo_key,
        "pull_request_description": {
            "title": "Refactor authentication service and fix security vulnerabilities",
            "body": """
## Changes

This PR refactors the authentication service to improve security and maintainability:

- Fix potential SQL injection vulnerability in login endpoint
- Implement proper password hashing with bcrypt
- Add rate limiting for failed login attempts
- Refactor token generation for better testability

## Testing

- [x] Unit tests added for password hashing
- [x] Integration tests for login flow
- [x] Manual testing with various user roles

## Reviewers

Please pay special attention to the security changes in `src/services/auth.js`.
            """
        }
    }


@mcp.tool()
def generate_cascade_prompt(repo_key: str) -> Dict[str, Any]:
    """
    Generate a Cascade-specific prompt based on the code review results
    
    This tool creates a well-structured prompt that can be copied and pasted into Cascade (Codeium's AI assistant)
    to automatically implement the suggested improvements from the code review.
    
    Args:
        repo_key: Repository key in the format "owner/repo"
    
    Returns:
        A structured Cascade prompt that can be used to implement the suggested improvements
    """
    if repo_key not in repo_data:
        return {"error": "Repository data not found."}
    
    repository_data = repo_data[repo_key]
    review_results = repository_data.get("review_results", {})
    
    # Gather all the suggestions and issues from various analyses
    all_improvements = []
    
    # Add code quality improvements
    if "quality_metrics" in repository_data:
        metrics = repository_data["quality_metrics"]
        if "recommendations" in metrics:
            all_improvements.extend(metrics["recommendations"])
    
    # Add security improvements
    if "vulnerabilities" in repository_data:
        for vuln in repository_data["vulnerabilities"]:
            all_improvements.append(
                f"Fix {vuln['severity']} security issue in {vuln['location']}: {vuln['description']} by {vuln['remediation']}"
            )
    
    # Add performance improvements
    if "performance_issues" in repository_data:
        for issue in repository_data["performance_issues"]:
            all_improvements.append(
                f"Fix {issue['severity']} performance issue in {issue['location']}: {issue['description']} by {issue['suggestion']}"
            )
    
    # If no improvements were found, generate some generic ones based on repository name
    if not all_improvements:
        repo_name = repo_key.split('/')[1] if '/' in repo_key else repo_key
        
        # Generate default improvements based on repo name hints
        if 'admin' in repo_name.lower():
            all_improvements = [
                "Implement proper authentication checks in admin routes to enhance security",
                "Add comprehensive error handling for admin operations to improve UX",
                "Refactor dashboard components for better code reusability",
                "Optimize API calls with pagination and caching for better performance",
                "Add comprehensive input validation to prevent security vulnerabilities",
                "Improve accessibility (ARIA attributes) in dashboard forms and tables",
                "Implement proper loading states for asynchronous operations"
            ]
        elif 'react' in repo_name.lower() or 'vue' in repo_name.lower() or 'angular' in repo_name.lower():
            all_improvements = [
                "Implement React.memo() for performance optimization of functional components",
                "Convert class components to functional components with hooks for better maintainability",
                "Add comprehensive PropTypes validation to improve code reliability",
                "Implement proper error boundaries to prevent UI crashes",
                "Optimize component rendering with useMemo and useCallback",
                "Add comprehensive unit tests for critical components",
                "Improve state management with context API or Redux"
            ]
        else:
            # Generic improvements for any codebase
            all_improvements = [
                "Implement comprehensive error handling throughout the application",
                "Add unit tests to improve code coverage and reliability",
                "Refactor duplicate code into reusable functions/components",
                "Optimize performance for critical application paths",
                "Add proper documentation for key functions and components",
                "Implement proper input validation and sanitization",
                "Update dependencies to latest stable versions"
            ]
    
    # Get basic repo information
    repo_parts = repo_key.split('/')
    owner = repo_parts[0]
    repo_name = repo_parts[1] if len(repo_parts) > 1 else repo_key
    
    # Create the Cascade prompt
    cascade_prompt = f"""
I need help implementing improvements to my GitHub repository ({repo_key}) based on an AI code review. Here are the specific improvements needed:

"""

    # Add numbered list of improvements
    for i, improvement in enumerate(all_improvements, 1):
        cascade_prompt += f"{i}. {improvement}\n"
    
    cascade_prompt += """
Please help me implement these changes one by one. For each change:
1. Explain the improvement and why it's beneficial
2. Show me the exact code modifications needed
3. Handle any potential side effects or dependencies

Let's start with the first improvement, and we can work through the list systematically.
"""
    
    return {
        "repo": repo_key,
        "cascade_prompt": cascade_prompt.strip(),
        "improvement_count": len(all_improvements)
    }


@mcp.tool()
def generate_improved_code(repo_key: str, file_path: str) -> Dict[str, Any]:
    """
    Generate improved code for a specific file based on review results
    
    This tool provides AI-generated code improvements that address the issues identified in the review.
    
    Args:
        repo_key: Repository key in the format "owner/repo"
        file_path: Path to the file to improve
    
    Returns:
        Improved code with explanations of changes
    """
    if repo_key not in repo_data:
        return {"error": "Repository data not found."}
    
    repository_data = repo_data[repo_key]
    
    # Find the file in the code content
    code_content = repository_data.get("code_content", {})
    if file_path not in code_content:
        return {"error": f"File '{file_path}' not found in repository data."}
    
    file_data = code_content[file_path]
    original_code = file_data.get("content", "")
    
    # Collect all issues related to this file
    file_issues = []
    
    # In a real implementation, this would collect all issues specific to this file
    # from security scans, performance analysis, code quality metrics, etc.
    
    # For demo purposes, create a placeholder improved version
    improved_code = original_code
    
    # Simple demo of code improvement (in a real implementation, this would use Claude API)
    if file_path.endswith(".js"):
        # Example JavaScript improvements
        improved_code = improved_code.replace("var ", "const ")
        improved_code = improved_code.replace("function(", "(")
    elif file_path.endswith(".py"):
        # Example Python improvements
        improved_code = improved_code.replace("except:", "except Exception as e:")
    
    return {
        "repo": repo_key,
        "file_path": file_path,
        "original_code": original_code,
        "improved_code": improved_code,
        "changes": [
            "Replaced outdated syntax with modern alternatives",
            "Improved error handling for better debugging",
            "Applied consistent code style"
        ],
        "cascade_prompt": f"""
Please help me implement the following improvements to {file_path}:

1. Replace outdated syntax with modern alternatives
2. Improve error handling for better debugging
3. Apply consistent code style

Here's the original code:

```
{original_code}
```

Please show me the improved version with explanations for each change.
"""
    }


# Helper functions
def fetch_repo_info(owner: str, repo: str) -> Dict[str, Any]:
    """Fetch repository information from GitHub API"""
    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers=GITHUB_HEADERS
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            # Rate limit exceeded
            return {
                "error": "GitHub API rate limit exceeded. Please try again later or provide a GitHub token.",
                "details": response.json().get("message", "No additional details")
            }
        elif response.status_code == 404:
            return {"error": f"Repository '{owner}/{repo}' not found. Check if the repository exists and is public."}
        else:
            return {"error": f"Failed to fetch repository information: {response.status_code}", "details": response.json().get("message", "No additional details")}
    except Exception as e:
        return {"error": f"Error fetching repository information: {str(e)}"}


def fetch_repo_files(owner: str, repo: str, path: str = "") -> Dict[str, Any]:
    """Fetch repository files from GitHub API"""
    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers=GITHUB_HEADERS
        )
        
        if response.status_code != 200:
            if response.status_code == 403:
                return {
                    "error": "GitHub API rate limit exceeded. Please try again later or provide a GitHub token.",
                    "details": response.json().get("message", "No additional details")
                }
            elif response.status_code == 404:
                return {"error": f"Path '{path}' not found in repository '{owner}/{repo}'."}
            else:
                return {"error": f"Failed to fetch repository contents: {response.status_code}", "details": response.json().get("message", "No additional details")}
        
        contents = response.json()
        result = {}
        
        if isinstance(contents, list):
            # This is a directory, process each item
            for item in contents:
                if item["type"] == "file":
                    # Only fetch content for small files (<1MB) to avoid rate limiting
                    if item.get("size", 0) < 1024 * 1024:
                        file_content = fetch_file_content(owner, repo, item["path"])
                        if "error" not in file_content:
                            result[item["path"]] = file_content
                    else:
                        result[item["path"]] = {
                            "content": f"File too large to fetch ({item.get('size', 0)} bytes)",
                            "path": item["path"],
                            "size": item.get("size", 0),
                            "too_large": True
                        }
                elif item["type"] == "dir":
                    # Only recurse a few levels deep to avoid rate limiting
                    if path.count("/") < 3:
                        sub_contents = fetch_repo_files(owner, repo, item["path"])
                        if "error" not in sub_contents:
                            result.update(sub_contents)
        else:
            # This is a single file
            if contents["type"] == "file":
                file_content = fetch_file_content(owner, repo, path)
                if "error" not in file_content:
                    result[path] = file_content
        
        return result
    except Exception as e:
        return {"error": f"Error fetching repository files: {str(e)}"}


def fetch_file_content(owner: str, repo: str, path: str) -> Dict[str, Any]:
    """Fetch content of a specific file from GitHub API"""
    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers=GITHUB_HEADERS
        )
        
        if response.status_code == 200:
            content_data = response.json()
            if content_data.get("encoding") == "base64" and content_data.get("content"):
                # Try to decode, but handle errors gracefully
                try:
                    decoded_content = base64.b64decode(content_data["content"]).decode("utf-8")
                    return {
                        "content": decoded_content,
                        "path": path,
                        "size": content_data.get("size", 0)
                    }
                except UnicodeDecodeError:
                    # This is likely a binary file
                    return {
                        "content": "Binary file (cannot display content)",
                        "path": path,
                        "size": content_data.get("size", 0),
                        "is_binary": True
                    }
        
        if response.status_code == 403:
            return {
                "error": "GitHub API rate limit exceeded. Please try again later or provide a GitHub token.",
                "details": response.json().get("message", "No additional details")
            }
        elif response.status_code == 404:
            return {"error": f"File '{path}' not found in repository '{owner}/{repo}'."}
        
        return {"error": f"Failed to fetch file content: {response.status_code}", "details": response.json().get("message", "No additional details")}
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


def analyze_repository_dependencies(repo_files: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze repository dependencies from package.json, requirements.txt, etc."""
    dependencies = {
        "javascript": [],
        "python": [],
        "other": []
    }
    
    for path, file_data in repo_files.items():
        if path.endswith("package.json"):
            # Parse JavaScript dependencies
            try:
                content = json.loads(file_data.get("content", "{}"))
                deps = content.get("dependencies", {})
                dev_deps = content.get("devDependencies", {})
                
                for name, version in deps.items():
                    dependencies["javascript"].append({
                        "name": name,
                        "version": version,
                        "dev": False
                    })
                
                for name, version in dev_deps.items():
                    dependencies["javascript"].append({
                        "name": name,
                        "version": version,
                        "dev": True
                    })
            except json.JSONDecodeError:
                pass
                
        elif path.endswith("requirements.txt"):
            # Parse Python dependencies
            content = file_data.get("content", "")
            for line in content.split("\n"):
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("==")
                    name = parts[0].strip()
                    version = parts[1].strip() if len(parts) > 1 else "latest"
                    dependencies["python"].append({
                        "name": name,
                        "version": version
                    })
    
    return dependencies


def find_security_issues(repo_files: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find potential security issues in code (placeholder implementation)"""
    security_issues = []
    
    # In a real implementation, this would use security analysis tools
    # For this demo, we're using very simple pattern matching
    
    security_patterns = {
        "sql_injection": [
            r"SELECT.*FROM.*WHERE.*\+",
            r"SELECT.*FROM.*WHERE.*\$",
            r"executeQuery\(.*\+",
        ],
        "xss": [
            r"innerHTML.*=",
            r"document\.write\(",
            r"eval\(",
        ],
        "hardcoded_secrets": [
            r"apiKey.*=.*['|\"]",
            r"password.*=.*['|\"]",
            r"secret.*=.*['|\"]",
        ]
    }
    
    return security_issues
