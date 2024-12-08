# Project Name: PowerPoint Generation API

## Overview

This project provides an API for generating PowerPoint presentations based on user inputs. Users can customize the presentation’s topic, description, slide content, and theme (fonts, colors, etc.) through various endpoints. The API also supports downloading the generated presentations in PPTX format.

---

## Prerequisites

Before running this project, ensure you have the following tools installed:

- Docker and Docker Compose
- Python 3.12+
- Redis
- PostgreSQL
- OpenAI API Key (for content generation)

---

## 1. **Clone the Repository**

Start by cloning this repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

---

## 2. **Environment Variables**

The application relies on environment variables configured in the `.env` file. A sample `.env` file is provided. Here are the key environment variables:

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

JWT_SIGNING_KEY=your-jwt-signing-key

DB_NAME=ppt_app
DB_USER=ppt_app
DB_PASSWORD=ppt_app
DB_HOST=ppt_db
DB_PORT=5432

# Redis settings
REDIS_URL=redis://redis:6379/0

# OpenAI API key
OPENAI_API_KEY=your-openai-api-key
PEXEL_API_KEY=your-pexel-api-key
```

Ensure you replace the placeholder values in the `.env` file with actual values before running the application.

---

## 3. **Access the Application**

To start the application, run the following command to build and start all containers:

```bash
docker-compose up --build
```

This will set up and start the following services:

- **Django App** (API server) on port 8000
- **PostgreSQL** (database)
- **Redis** (cache and message broker)

Once the containers are up and running, the API will be available at:

```bash
http://localhost:8000
```

You can start interacting with the API using the endpoints described below.

---

## 4. **Create a Superuser**

To create a superuser for accessing the Django admin panel, run the following command inside the running `ppt_generator` container:

```bash
docker-compose exec ppt_generator python manage.py createsuperuser
```

This will prompt you to enter a username, email address, and password for the superuser.

Once the superuser is created, you can access the Django admin panel by visiting:

```bash
http://localhost:8000/admin
```

Login with the superuser credentials.

---

## 5. **API Endpoints**

The application exposes the following API endpoints:

### **POST** `/api/v1/presentations/`
Create a new presentation.

**Request body:**

```json
{
  "topic": "New Presentation",
  "description": "A description of the presentation",
  "num_slides": 5,
  "theme": {
    "fonts": {
      "title_font": "Arial",
      "content_font": "Tahoma"
    },
    "font_sizes": {
      "title_size": 30,
      "content_size": 18
    },
    "colors": {
      "background_color": [255, 255, 255],
      "title_color": [0, 0, 0],
      "content_color": [0, 0, 0]
    }
  }
}
```

**Response:**

The response returns immediately after creating the presentation object and invokes an asynchronous backend process to generate the slide content for the PPT. 

While content generation is in progress, users can poll the status of the presentation using the **GET** request below. 

**Status values:**
- `pending`: Initial state.
- `in_progress`: Content generation in progress.
- `completed`: The presentation is ready for download.
- `failed`: The content generation failed.

### **GET** `/api/v1/presentations/{id}/`
Retrieve the details of a presentation by ID.

### **GET** `/api/v1/presentations/`
Retrieve all user presentations order by creatin time (recent first).

### **PUT** `/api/v1/presentations/{id}/`
Modify the presentation configuration.

**Request body:**

```json
{
  "num_slides": 5,
  "theme": {
    "fonts": {
      "title_font": "Verdana",
      "content_font": "Calibri"
    },
    "font_sizes": {
      "title_size": 36,
      "content_size": 20
    },
    "colors": {
      "background_color": [255, 255, 255],
      "title_color": [0, 0, 0],
      "content_color": [0, 0, 0]
    }
  }
}
```

**Note:** Updating `num_slides` (optional) will change the status to `pending` and trigger a re-run of the content generation step.

**Yet to implement:** The ability to modify the number of slides dynamically will trigger an update to the presentation content, but it's not currently functional.

### **GET** `/api/v1/presentations/{id}/download/`
Download the generated PowerPoint presentation in PPTX format.

---

## 6. **Rate Limiting**

To prevent abuse, rate limiting is applied:

- **5 requests per minute per user**

If the rate limit is exceeded, users will receive a `429 Too Many Requests` response.

---

## 7. **Authentication API**

The system supports JWT-based authentication. To obtain a token, use the following API:

### **POST** `/api/v1/auth/login/`
Login and retrieve a JWT token.

**Request body:**

```json
{
  "username": "your-username",
  "password": "your-password"
}
```

**Response:**

```json
{
  "token": "your-jwt-token"
}
```

This token should be included in the `Authorization` header for subsequent requests, e.g., `Authorization: Bearer <your-jwt-token>`.

---

## 8. **Slide Layouts**

The available slide layouts are (Auto selected by AI while creating PPT):

- **Title Slide**
- **Title and Content**
- **Section Header**
- **Two Content**
- **Comparison**
- **Title Only**
- **Blank**
- **Content with Caption**
- **Picture with Caption**
- **Title and Vertical Text**
- **Vertical Title and Text**

These layouts are used in the generated presentations to organize content in different formats.

---

## 9. **Allowed Theme Configuration**

The theme configuration allows users to define the fonts, font sizes, and colors used in the presentation. The available configurations are:

### **Fonts:**
- **title_font:** Options: "Lucida Console", "Arial", "Times New Roman", "Verdana"
- **content_font:** Options: "Calibri", "Arial", "Helvetica", "Georgia"

### **Font Sizes:**
- **title_size:** Range from 10 to 100
- **content_size:** Range from 8 to 72

### **Colors:**
- **background_color:** RGB values, e.g., `[255, 255, 255]`
- **title_color:** RGB values, e.g., `[0, 0, 0]`
- **content_color:** RGB values, e.g., `[0, 0, 0]`

---

## 10. **Running the Application with Docker Compose**

To run the application with Docker Compose, use the following command:

```bash
docker-compose up --build
```

This will build the containers and start the Django app, Redis, PostgreSQL, and other services. Once the services are running, you can access the API at `http://localhost:8000`.

To stop the services, use:

```bash
docker-compose down
```

---

## 11. **Testing the API**

You can test the API using tools like **Postman** or **cURL** to send requests to the endpoints described above. For example, to create a new presentation, use a **POST** request to `/api/v1/presentations/` with the request body mentioned in the API section.

---