# The Oklahoma Handyman

## Overview
The Oklahoma Handyman project is designed to streamline and enhance the management of handyman services for both business administrators and customers. It provides a user-friendly public website for customers to access services and an administrative interface for efficient business operations. This project includes three primary components:

- **Public Website**: [https://theoklahomahandyman.com](https://theoklahomahandyman.com)
- **Admin Interface**: [https://admin.theoklahomahandyman.com](https://admin.theoklahomahandyman.com)
- **Back-end API**: [https://api.theoklahomahandyman.com](https://api.theoklahomahandyman.com)

## Features

### Public Website
The public website serves as the primary interface for customers. Features include:
- Business information such as contact details, location, and an overview of handyman services offered, including repair, maintenance, and remodeling solutions tailored to both residential and commercial needs.
- A contact form that:
  - Creates a new customer if not already registered.
  - Creates a new order linked to the customer.

### Admin Interface
The admin interface allows administrators to manage various aspects of the business, including:
- Customer and admin information.
- Personal contact details.
- Material and tool purchases.
- Suppliers and their addresses.
- Inventory management (materials and tools).
- Service types.
- Work orders, including:
  - Categories of work.
  - Materials and tools used.
  - Labor and hours worked.
  - Line-item adjustments.
  - Workers assigned.
  - Payments and calculations (e.g., total, tax).

### Back-end API
The API powers the functionality of both the public and admin interfaces and provides:
- Authentication and authorization.
- Integration with AWS S3 for image and file storage.
- PostgreSQL database hosted on AWS RDS.
- Deployment on an AWS EC2 instance with Nginx and Gunicorn, secured via HTTPS using Certbot.

## Technology Stack

This technology stack was selected to optimize scalability, security, and maintainability, leveraging proven frameworks and cloud services for an efficient development and deployment process. By combining React, Django, and AWS infrastructure, the project ensures seamless integration, robust performance, and easy scalability for both the public website and admin interface.
### Back-end
- **Frameworks and Libraries**:
  - Django
  - Django REST Framework
  - Django CORS Headers
  - Django REST Framework SimpleJWT
  - Python-Dotenv
  - Pillow
  - Boto3
  - Coverage
  - Psycopg2-Binary
  - Python-Dateutil
  - Django Storages
- **Deployment**:
  - AWS EC2
  - Nginx
  - Gunicorn
  - Certbot
- **Storage**:
  - AWS S3 for images and files, chosen for its durability, scalability, and cost-effectiveness in handling static assets and backups.
  - AWS RDS (PostgreSQL), selected for its robust database management capabilities, high availability, and seamless integration with other AWS services.
- **Environment Configuration**:
  - Python virtual environment

### Front-end
- **Admin Interface**:
  - Built with React and Vite
  - Uses libraries including:
    - Axios
    - Chart.js
    - DataTables.net
    - Font Awesome
    - jQuery
    - JWT Decode
    - React-Toastify
- **Public Website**:
  - Built with React and Vite
  - Uses libraries including:
    - Axios
    - Bootstrap
    - JWT Decode
    - React-Bootstrap
    - React-Toastify
- **Deployment**:
  - AWS S3 and CloudFront
  - AWS Route 53 for DNS
  - AWS Certificate Manager for HTTPS

## Dependencies

### Back-end (requirements.txt)
```
asgiref
boto3
botocore
coverage
Django
django-cors-headers
django-storages
djangorestframework
djangorestframework-simplejwt
jmespath
pillow
psycopg2-binary
PyJWT
python-dateutil
python-dotenv
pytz
s3transfer
six
sqlparse
tzdata
urllib3
```

### Public Website (package.json)
```json
{
  "name": "public",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.7.7",
    "bootstrap": "^5.3.3",
    "js-cookie": "^3.0.5",
    "jwt-decode": "^4.0.0",
    "react": "^18.3.1",
    "react-bootstrap": "^2.10.4",
    "react-dom": "^18.3.1",
    "react-toastify": "^10.0.5"
  },
  "devDependencies": {
    "@eslint/js": "^9.9.0",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "eslint": "^9.9.0",
    "eslint-plugin-react": "^7.35.0",
    "eslint-plugin-react-hooks": "^5.1.0-rc.0",
    "eslint-plugin-react-refresh": "^0.4.9",
    "globals": "^15.9.0",
    "vite": "^5.4.1"
  }
}
```

### Admin Interface (package.json)
```json
{
  "name": "admin",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.7.7",
    "chart.js": "^4.4.4",
    "datatables.net-bs4": "^2.1.5",
    "datatables.net-dt": "^2.1.5",
    "datatables.net-responsive-dt": "^3.0.3",
    "font-awesome": "^4.7.0",
    "jquery": "^3.7.1",
    "js-cookie": "^3.0.5",
    "jwt-decode": "^4.0.0",
    "react": "^18.3.1",
    "react-chartjs-2": "^5.2.0",
    "react-dom": "^18.3.1",
    "react-router": "^6.26.1",
    "react-router-dom": "^6.26.1",
    "react-toastify": "^10.0.5"
  },
  "devDependencies": {
    "@eslint/js": "^9.9.0",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "eslint": "^9.9.0",
    "eslint-plugin-react": "^7.35.0",
    "eslint-plugin-react-hooks": "^5.1.0-rc.0",
    "eslint-plugin-react-refresh": "^0.4.9",
    "globals": "^15.9.0",
    "vite": "^5.4.1"
  }
}
```

## Deployment
- **Infrastructure**: The project is deployed using AWS services, including EC2, S3, CloudFront, RDS, VPC, IAM, Route 53, and Certificate Manager.
- **Security**: HTTPS is enabled using Certbot and AWS Certificate Manager.
- **Scalability**: AWS VPC and IAM are used for secure and scalable deployment.

## Usage
### Public Website
- Visit [https://theoklahomahandyman.com](https://theoklahomahandyman.com) to explore services or submit a contact form.

### Admin Interface
- Access [https://admin.theoklahomahandyman.com](https://admin.theoklahomahandyman.com) to manage business operations.

### API
- The API is hosted at [https://api.theoklahomahandyman.com](https://api.theoklahomahandyman.com).

---

We welcome contributions to this project! Whether you're interested in enhancing existing features, fixing bugs, or adding new functionality, please feel free to submit pull requests. Additionally, if you encounter issues or have suggestions, we encourage you to raise them in the issues section. For more information, please review our [Contribution Guidelines](CONTRIBUTING.md).
