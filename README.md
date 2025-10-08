# Loonflow 3.0 - Intelligent and Visual Process Automation System
Dedicated to providing enterprise-grade unified workflow solutions

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)
[![MUI](https://img.shields.io/badge/MUI-5.x-007FFF?logo=mui&logoColor=white)](https://mui.com/)
[![License](https://img.shields.io/badge/license-AGPL%20v3-blue)](https://www.gnu.org/licenses/agpl-3.0)

[English](./README.md) | [简体中文](./README_zh.md)

# 🚀 Loonflow 3.0 - A Fresh Start

> **Important Notice**: Due to significant changes in version 3.0 and tight development schedule, the current version may have some known issues. I will take a week's rest (8 days of intensive development has been quite exhausting) and then quickly fix all issues. Thank you for your understanding and support!

Loonflow is an open-source process automation platform developed based on Django. After multiple versions of iteration and refactoring, we proudly present Loonflow 3.0 - a version that achieves a qualitative leap in visualization, flexibility, and scalability.

The core of version 3.0 is "making complex business processes simple and visual, making personalized customization needs within reach." Not only have we rebuilt the process and form designers, but we have also constructed a powerful extension framework, aiming to become the most core process engine in enterprise digital transformation.

# Feature Demo
[![Feature Demo](https://img.youtube.com/vi/IpLePpajyfU/0.jpg)](https://www.youtube.com/watch?v=IpLePpajyfU)


# ✨ Core Features

## 🎯 Revolutionary Visual Design
- **Drag-and-Drop Process Designer**: No complex configuration needed. Complete complex business process modeling through intuitive drag-and-drop connections. Supports advanced nodes like conditional branches, parallel tasks, and hooks.
- **Smart Form Designer**: Powerful visual form building tool with rich field types (text, numbers, dropdowns, personnel selection, attachments, etc.) and flexible layouts.
- **Real-time Preview & Validation**: Real-time preview during process design with built-in process logic validation to prevent design errors early.
- **Multi-Version Process Configuration**: You can configure multiple versions of processes and easily test and switch between versions.


## 🔧 Ultimate Flexibility & Extensibility
- **Plugin Architecture**: We provide plugin extension capabilities for almost all key nodes (such as custom actions, permission validation, notification methods, etc.). Your unique business logic can be easily integrated like building blocks.
- **Powerful API System**: Provides comprehensive and clear RESTful APIs for seamless integration with your customer service systems, CMDB, monitoring systems, CI/CD, OA, and other third-party systems.
- **Highly Customizable Permission Model**: Supports fine-grained permission control based on roles, departments, or even specific business conditions to meet complex enterprise permission management needs.

## 💼 Enterprise-Ready Features Out of the Box
- **Multi-Type Ticket Support**: Easily manage various processes including IT operations, HR approvals, financial reimbursements, customer service, etc.
- **Automation & Smart Routing**: Supports conditional routing based on form data, automatic assignee assignment, and intelligent ticket flow.
- **Comprehensive Audit Logs**: Complete records of every operation from ticket creation to closure, meeting compliance and audit requirements.
- **Multi-Tenant Support (Optional)**: Provides data isolation capabilities for SaaS providers or large enterprise groups (requires additional authorization).

# 🛠️ Installation & Deployment
1. Download docker-compose related files
```
wget https://github.com/blackholll/loonflow/blob/v3.0.1_mui/docker_compose_deploy/docker-compose.yml
wget https://github.com/blackholll/loonflow/blob/v3.0.1_mui/docker_compose_deploy/.env
```
2. Modify the .env file
Please modify at least the password section
3. Start docker-compose
Navigate to the directory containing docker-compose.yml and execute:
```
docker-compose up -d
```
4. Create admin user
```
cd /app/loonflow
python manage.py createsuperuser
```
5. Access loonflow
Login to loonflow using the email and password you created in step 3

# 🗺️ Project Roadmap

## 🎯 Version 3.1.0 (November-December 2025)
### Core Feature Enhancements
- 📝 **Form Field Extensions** - New file upload, external data source, rich text editor field types
- ⏰ **Process Timeout Control** - Support for automatic node timeout transitions, improving process automation
- 🔍 **Full-Text Search** - Implement full-text search functionality for tickets and processes
- 📋 **Workflow Classification** - Support workflow classification management for better organization

### Enterprise Integration
- 🔐 **OAuth Authentication** - Integrate with mainstream enterprise authentication (WeChat Work, Feishu, DingTalk, Azure, etc.)
- 📢 **Message Notifications** - Support message push to WeChat Work, DingTalk, Feishu, Teams and other platforms
- 🔗 **Sub-Ticket Generation** - Support rule-based automatic sub-ticket generation for complex business processes

### Permissions & Security
- 🛡️ **Fine-Grained Permissions** - Field-level permission control, supporting hide, desensitization, processing operations
- 👥 **Creation Permission Control** - Fine-grained configuration of workflow creation permissions
- 📊 **Hook Event Logging** - Complete Hook event query and audit functionality

### Development & Documentation
- 📚 **ReadTheDocs Documentation** - Complete online documentation system
- 🧪 **Unit Testing** - Complete frontend and backend unit test coverage
- 🌐 **Backend Internationalization** - Backend API internationalization support
- 🐛 **Bug Fixes** - Continuous issue fixes and minor feature optimizations

## Medium-term Planning (March-June 2026)
- 🚀 **Performance Optimization** - Optimize system performance for large data volume scenarios
- 🔌 **Plugin Ecosystem** - Enrich official plugin library, support more business scenarios
- 📱 **Mobile Adaptation** - Optimize user experience on mobile devices
- 🌐 **Multi-Language Internationalization** - Complete multi-language interface support

## Long-term Vision (Second Half of 2026)
- 🤖 **AI Integration** - Integrate AI capabilities, provide intelligent process suggestions and automation, intelligent ticket data analysis, knowledge Q&A based on tickets
- 🔗 **Ecosystem Integration** - Deep integration with more mainstream enterprise systems
- 📊 **Data Analytics** - Provide process data analysis and optimization suggestions
- 🏢 **Enterprise Features** - Enhanced enterprise deployment and management capabilities

# 📖 Deep Dive

- 📚 **Complete Documentation** - Learn all the details about installation, configuration, usage, and development.
- 🎬 **Usage Tutorials** - Step-by-step guide on how to configure a complete IT operations ticket process.
- 🔌 **Hook Development Guide** - Learn how to develop custom plugins for Loonflow.
- 🌐 **API Reference** - View complete API interface documentation.

# 🤝 Contributing

Community contributions are warmly welcome! Whether you're fixing typos, improving documentation, reporting bugs, or developing new features.

Please fork this repository first, then submit a Pull Request.

# ❓ Getting Help

- 📝 **GitHub Issues** - Submit bug reports and feature requests.
- 💬 **Discussion Forum** (Coming Soon) - Communicate with the community and other users.
- 📧 **Commercial Support & Customization**: For enterprise-level deep customization, technical training, or deployment support needs, please contact me at [blackholll@163.com;blackholll.cn@gmail.com].
- 💰 **Member Benefits**

# Member Benefits (One-time support available to enjoy monthly benefits)
Click the "sponsor" button on the GitHub project homepage to sponsor. If your are from China. go to [简体中文](./README_zh.md), check alipay method to donate.


## Community Partner - $5/month
Suitable for everyone who appreciates my work and hopes it thrives.
- 🛡️ Get exclusive identity group in my official Discord community

## Core Contributor - $10/month
Suitable for heavy users who rely on this project and want to participate more deeply.

- ✅ Enjoy all benefits from the previous tier.
- 🎧 Entry & Annual Call: First-time sponsors get 30 minutes of voice/video Q&A, and then one 60-minute Q&A session annually.

## Project Collaborator - $50/month
Suitable for professionals and small teams whose workflows are closely related to the healthy development of this project.
- ✅ Enjoy all benefits from the previous tier.
- 🔥 Priority Processing: Your bug reports or feature requests will be moved to the priority development queue.
- 🎧 Enhanced Annual Support: Enjoy a total of 3 sessions of 60-minute voice/video Q&A annually for in-depth problem discussion or strategy planning.

## Strategic Sponsor - $100/month
Tailored for enterprises that want to ensure project success and gain significant brand exposure.

- ✅ Enjoy all benefits from the previous tier.
- 🌐 Prominent Display: Your company's logo will be displayed as a key supporter in a prominent position on the project's GitHub homepage.
- 🎧 Exclusive Annual Support: Enjoy a total of 10 sessions of 60-minute voice/video Q&A annually for continuous exclusive technical support.


# 🙏 Acknowledgments

Thanks to all contributors who have contributed code, submitted issues, and helped improve documentation for Loonflow.

If Loonflow has been helpful to you, please give us a ⭐️ Star for support!

# Welcome Donations
Your support is my greatest motivation. 

# License & Legal Notice
This project is open source under the AGPLv3 license. You are free to view, modify, and distribute the code, but please note:

If you provide this project as a SaaS service to the public, according to AGPLv3, you must open source all your modifications.

If you want to use this project for SaaS services without open-sourcing modifications, or if you need to use its multi-tenant functionality within your enterprise, you need to obtain a commercial license from us. Please contact [blackholll@163.com;blackholll.cn@gmail.com].
