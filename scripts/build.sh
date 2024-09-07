poetry export -f requirements.txt --output requirements.txt --without-hashes
cd frontend
npm run build
cd ..
# sudo docker build -f Dockerfile -t memory-prd .