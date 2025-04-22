# GitHub Code Review MCP

An MCP (Model Context Protocol) service that enables AI-powered code reviews of GitHub repositories using Claude.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that enables seamless integration between LLM applications and external data sources and tools. Whether you're building an AI-powered IDE, enhancing a chat interface, or creating custom AI workflows, MCP provides a standardized way to connect LLMs with the context they need.

## Overview

This service provides a set of tools that allow users to:

1. Submit GitHub repositories for code review
2. Get detailed feedback and suggestions on their codebase
3. Focus reviews on specific areas of interest (e.g., security, performance, best practices)
4. Track review history and access previous reviews

## Features

- **Repository Analysis**: Analyze GitHub repositories by simply providing the URL
- **Focused Reviews**: Specify areas to focus the code review on
- **Improvement Suggestions**: Get specific suggestions for improving the codebase
- **File-Level Analysis**: Get detailed feedback for specific files
- **Security Scanning**: Identify security vulnerabilities and get remediation advice
- **Dependency Analysis**: Analyze project dependencies for outdated packages and vulnerabilities
- **Code Quality Metrics**: Get insights into code complexity, duplication, and maintainability
- **Performance Analysis**: Identify performance bottlenecks and optimization opportunities
- **Best Practices Comparison**: Compare code against industry best practices for your framework
- **PR Description Generator**: Automatically generate comprehensive pull request descriptions
- **Cascade Prompt Generation**: Create ready-to-use prompts for implementing improvements with Cascade

## MCP Tools

This MCP server provides the following tools:

### Repository Review Tools
- **`review_repository(repo_url: str, focus_areas: Optional[str] = None)`**: Review a GitHub repository by providing the URL. You can optionally specify areas to focus on (e.g., "security, performance, best practices").

- **`list_reviewed_repos()`**: List all repositories that have been reviewed, including review dates and focus areas.

- **`get_review_details(repo_key: str)`**: Get detailed review results for a specific repository using its key in the format "owner/repo".

### Improvement and Analysis Tools
- **`suggest_improvements(repo_key: str, file_path: Optional[str] = None)`**: Get specific improvement suggestions for an entire repository or a specific file.

- **`analyze_dependencies(repo_key: str)`**: Analyze repository dependencies to identify outdated packages, potential vulnerabilities, and provide recommendations.

- **`scan_security_vulnerabilities(repo_key: str)`**: Scan a repository for security vulnerabilities and provide remediation steps.

- **`analyze_code_quality(repo_key: str)`**: Get code quality metrics including complexity, duplication, and maintainability scores.

- **`analyze_performance(repo_key: str)`**: Identify performance bottlenecks and get optimization suggestions.

- **`compare_with_best_practices(repo_key: str, framework: Optional[str] = None)`**: Compare code against industry best practices, with optional framework-specific comparisons.

### Code Generation Tools
- **`generate_pull_request_description(repo_key: str, review_id: str)`**: Generate a comprehensive pull request description based on code review results.

- **`generate_cascade_prompt(repo_key: str)`**: Create a Cascade-specific prompt that can be used to implement the suggested improvements.

- **`generate_improved_code(repo_key: str, file_path: str)`**: Generate improved code for a specific file based on the review results.

## Installation

### Prerequisites

- Python 3.12 or higher
- MCP 1.6.0 or higher

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/kl63/Mcp-Server-Demo.git
   cd Mcp-Server-Demo
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -e .
   ```

4. (Optional) Set up GitHub API token:
   
   To avoid GitHub API rate limiting, it's recommended to set up a GitHub API token:
   
   - Create a Personal Access Token on GitHub (Settings > Developer settings > Personal access tokens)
   - Set the token as an environment variable:
     ```bash
     export GITHUB_API_TOKEN=your_github_token  # On Windows: set GITHUB_API_TOKEN=your_github_token
     ```
   
   Without a token, you'll be limited to 60 requests per hour, which may not be enough for analyzing larger repositories.

## Usage

### Starting the MCP Server

Run the following command to start the MCP server:

```bash
python main.py
```

### Using the Service with Claude

Once the MCP server is running, you can interact with it through Claude by using commands like:

1. Review a repository:
   ```
   Please review the GitHub repository at https://github.com/username/repo-name
   ```

2. Focus on specific areas:
   ```
   Review https://github.com/username/repo-name with focus on security and performance
   ```

3. Get improvement suggestions:
   ```
   Suggest improvements for the repository https://github.com/username/repo-name
   ```

4. List previously reviewed repositories:
   ```
   Show me all the repositories that have been reviewed
   ```

5. Generate a Cascade prompt for implementing improvements:
   ```
   Generate a Cascade prompt for the improvements to https://github.com/username/repo-name
   ```

6. Get improved code for a specific file:
   ```
   Show me improved code for the file src/components/Button.js in https://github.com/username/repo-name
   ```

## License

MIT

## References

- [Model Context Protocol (MCP) Python SDK](https://github.com/modelcontextprotocol/python-sdk) - The official Python SDK for building MCP providers