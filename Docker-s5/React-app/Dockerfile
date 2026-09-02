# Use Node.js as base image to fulfill the Node/React requirement
FROM node:alpine

# Install a simple static server
RUN npm install -g http-server

# Create app directory
WORKDIR /app

# Copy the React HTML file
COPY index.html ./

# Expose port
EXPOSE 80

# Run the server
CMD ["http-server", "-p", "80"]
