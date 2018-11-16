#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<html><head><title>EC2 LAB</title></head><body>Hello world!</body></html>" > /var/www/html/index.html
