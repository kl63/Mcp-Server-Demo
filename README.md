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

## API Tools

The service exposes the following MCP tools:

- `review_repository(repo_url, focus_areas)`: Review a GitHub repository
- `list_reviewed_repos()`: List all repositories that have been reviewed
- `get_review_details(repo_key)`: Get detailed review results for a specific repository
- `suggest_improvements(repo_key, file_path)`: Suggest specific improvements for a repository or file
- `analyze_dependencies(repo_key)`: Analyze repository dependencies and provide recommendations
- `scan_security_vulnerabilities(repo_key)`: Scan for security issues and vulnerabilities
- `analyze_code_quality(repo_key)`: Get code quality metrics and suggestions
- `analyze_performance(repo_key)`: Identify performance issues and optimization opportunities
- `compare_with_best_practices(repo_key, framework)`: Compare against industry best practices
- `generate_pull_request_description(repo_key, review_id)`: Generate comprehensive PR descriptions
- `generate_cascade_prompt(repo_key)`: Create a prompt for implementing improvements with Cascade
- `generate_improved_code(repo_key, file_path)`: Generate improved code for a specific file

## Note on Limitations

This implementation includes placeholders for the actual Claude API integration. In a production environment, you would need to:

1. Integrate with a proper Claude API endpoint
2. Implement token handling and rate limiting
3. Potentially add caching for repository data
4. Add authentication for GitHub API requests

## License

MIT

## References

- [Model Context Protocol (MCP) Python SDK](https://github.com/modelcontextprotocol/python-sdk) - The official Python SDK for building MCP providers