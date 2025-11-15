Weather-app-Tech-Assessment
🌍 Real-Time Weather App
Built by Sylvia Karanja 💙

This is a responsive, interactive weather application built with Streamlit. It fetches real-time weather data and 5-day forecasts using the WeatherAPI and allows users to save weather records to a local database. Designed as part of the Software Engineer Intern - AI/ML Application technical assessment.

✨ Features
🔍 Search weather by location (city, zip code, or landmark)
📍 Option to use current location (IP-based)
🌡️ Toggle between Celsius (°C) and Fahrenheit (°F)
☀️ Display current weather conditions with icons
📅 Show 5-day forecast with daily summaries
💾 Save weather data to database with date range selection
✅ Validates date inputs before saving
🧹 Delete saved records (if implemented)
📘 Sidebar info about PM Accelerator and author credit
🧠 About PM Accelerator
This app includes an info section describing PM Accelerator, a product management training and mentorship program.
Learn more on their LinkedIn page.

🛠️ Tech Stack
Tool	Purpose
Python	Core programming language
Streamlit	Web app framework
WeatherAPI	Real-time weather data source
SQLite	Local database for saved records
VS Code	Development environment
🚀 Setup Instructions
Clone the repository

git clone https://github.com/your-username/weather-app
cd weather-app
2. Install independencies pip install -r requirements.txt

3. Add your WeatherAPI key

Create a .env file or insert your API key directly in the script: WEATHER_API_KEY = "your_api_key_here"

4.Run the app streamlit run weather_app.py 

🧪 Testing- Try searching for "Nairobi" or "Eiffel Tower"
Use the calendar pickers to select a date range
Click Save to Database and confirm success
Check sidebar for author info and PM Accelerator details

📬 Contact For questions or collaboration, reach out to Sylvia Karanja via GitHub.📄 LicenseThis project is for educational and assessment purposes only.
Let me know if you want to include screenshots, deployment instructions (e.g. Streamlit Cloud), or a section on future improvements. You’re ready to submit this with confidence! 
