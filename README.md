# Journalist-Scraping-EC2

## 📌 Project Overview
This project automates web scraping of journalist data from [CPJ.org](https://cpj.org/data/?status=Killed&start_year=1992&end_year=2025&group_by=year&motiveConfirmed%5B%5D=Confirmed&type%5B%5D=Journalist). The scraper is deployed on an AWS EC2 instance using Selenium.

## 🚀 Features
- **Automated Multi-Page Scraping**: Extracts journalist data across multiple pages.
- **Selenium for Dynamic Content**: Handles JavaScript-rendered pages.
- **AWS EC2 Deployment**: Runs the scraper remotely.
- **Data Export**: Saves results in CSV or Excel format for analysis.
- **Logging & Error Handling**: Ensures reliability and debugging support.

## 🛠️ Technologies Used
- **Python**
- **Selenium**
- **AWS EC2**
- **Pandas** (for data handling)
- **Git & GitHub** (for version control)

## 📂 Project Structure
```
Journalist-Scraping-EC2/
│-- scrape_data.py  # Main scraping script
│-- requirements.txt  # Required Python libraries
│-- output/  # Folder containing scraped data files
│-- logs/  # Folder storing logs
│-- README.md  # Project documentation
```

## 🔧 Setup & Installation
### **1️⃣ Clone the Repository**
```sh
git clone git@github.com:AdarshRG09/Journalist-Scraping-EC2.git
cd Journalist-Scraping-EC2
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Run the Scraper**
```sh
python scrape_data.py
```

## 🚀 Deploying on AWS EC2
### **1️⃣ Connect to EC2 Instance**
```sh
ssh -i "path/to/adarsh.pem" ubuntu@<ec2-public-ip>
```

### **2️⃣ Transfer Files to EC2**
```sh
scp -i "path/to/adarsh.pem" -r * ubuntu@<ec2-public-ip>:~/Journalist-Scraping-EC2/
```

### **3️⃣ Run on EC2**
```sh
cd Journalist-Scraping-EC2
python3 scrape_data.py
```

## 📊 Output Example
| Date | Journalist Name | Country | Status |
|------|---------------|---------|--------|
| 2024-02-15 | John Doe | USA | Killed |
| 2024-02-20 | Jane Smith | UK | Killed |

## 🤝 Contributing
Feel free to fork this repository and submit a pull request if you have improvements!

## 📜 License
This project is licensed under the MIT License.

---
🔗 **Author:** AdarshRG09  
📧 **Contact:** adarshhockey09@gmail.com  
