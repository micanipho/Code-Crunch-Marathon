# 🌧️ Rain Alert - README

Welcome to **Rain Alert**! This project leverages the **OpenWeather API** to detect whether rain is expected in a user's area and notifies the user via **SMS using Twilio**.

---

## 📋 Table of Contents  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [To-Do](#to-do)  
- [Contributing](#contributing)  
- [License](#license)

---

## ⚡ Features  
- Detect rain forecast using the **OpenWeather API**.  
- Retrieve and use the user's **current location**.  
- Send real-time SMS alerts using **Twilio**.  
- Clean and simple code structure for easy maintenance.

---

## ✅ Prerequisites  
Before you begin, ensure you have the following installed:

1. **Python 3.x**  
2. **pip** (Python package manager)  
3. **Twilio account** – [Sign up here](https://www.twilio.com/try-twilio)  
4. **OpenWeather API Key** – [Generate your key here](https://openweathermap.org/api)

---
 ## Usage

1. Create **Twilio account** – [Sign up here](https://www.twilio.com/try-twilio)  
2. Get your **OpenWeather API Key** – [Generate your key here](https://openweathermap.org/api)
3. At the root folder craete a .env file and store your credentials in this format:
```bash 
ACCOUNT_SID= {acoount_sid}
AUTH_TOKEN={auth_token}
API_KEY={api_key}
MESSAGE_SERVICE_SID={service_sid}
CELL_NUMBER={verified number on twilio}
```