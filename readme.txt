git clone
cd
docker build -t backtesting-app .
docker run -p 8080:5000 -e POLYGON_API_KEY=6u512poKFdRFB7PZpgNGSVqj5pVvYner backtesting-app
http://localhost:8080/
