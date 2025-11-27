# Contributing to AI Intern for Twitter Support

Thank you for your interest in this project!

## 🔒 Proprietary Notice

This is **proprietary software** owned by @DecentralizedJM. All rights are reserved.

## ✅ What You Can Do

While this is a proprietary project, contributions are welcome in the following ways:

### Bug Reports
- Open an issue with detailed reproduction steps
- Include error messages and logs
- Describe expected vs actual behavior

### Feature Suggestions
- Open an issue with the `enhancement` label
- Explain the use case and benefit
- Provide examples if applicable

### Documentation Improvements
- Fix typos or unclear explanations
- Add examples or clarifications
- Improve setup instructions

## ❌ What Requires Permission

The following require explicit written permission from the author:

- Commercial use or redistribution
- Creating derivative products
- Integrating into paid services
- Removing attribution or copyright notices

## 📝 How to Contribute

### Reporting Issues

1. Check existing issues first
2. Use the issue template
3. Provide:
   - Environment details (OS, Python version)
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error logs

### Suggesting Features

1. Open an issue with `enhancement` label
2. Describe:
   - Problem you're trying to solve
   - Proposed solution
   - Alternative solutions considered
   - Additional context

### Code Contributions

**Note:** All code contributions will be owned by @DecentralizedJM upon acceptance.

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** with clear commits
4. **Test thoroughly**: 
   ```bash
   python demo_auto.py
   python test_bot.py
   ./test_n8n.sh
   ```
5. **Submit a Pull Request**:
   - Clear description of changes
   - Link to related issues
   - Screenshots if applicable

### Pull Request Guidelines

- ✅ One feature/fix per PR
- ✅ Clear, descriptive commit messages
- ✅ Code follows existing style
- ✅ All tests pass
- ✅ Documentation updated if needed
- ✅ No breaking changes without discussion

## 🔍 Code Standards

### Python Style
- Follow PEP 8
- Use type hints where applicable
- Add docstrings to functions
- Keep functions focused and small

### Documentation
- Update README if adding features
- Add comments for complex logic
- Update .env.example if adding config

## 🧪 Testing Your Changes

Before submitting:

```bash
# Test automated demo
python demo_auto.py

# Test interactive CLI
python test_bot.py

# Test API server
python webhook_server.py
# In another terminal:
curl http://localhost:8000/

# Test n8n workflow (if applicable)
./test_n8n.sh
```

## 📧 Contact

For questions or permissions:
- GitHub Issues: https://github.com/DecentralizedJM/AI-Intern-for-twitter-support/issues
- GitHub Profile: [@DecentralizedJM](https://github.com/DecentralizedJM)

## 🙏 Acknowledgment

By contributing, you acknowledge that:
1. Your contributions become part of the proprietary codebase
2. Ownership remains with Jithin Mohandas (@DecentralizedJM)
3. You have the right to submit the contribution
4. You agree to the project's license terms

## ⚖️ License

See [LICENSE](LICENSE) file for complete terms.

All contributions are subject to the same proprietary license as the main project.

---

Thank you for helping make this project better! 🚀
