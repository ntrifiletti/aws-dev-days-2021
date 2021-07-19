# AWS Dev Days 2021
# Introduction

Organisations are adopting infrastructure as code to be more agile to business requirements. Configuration automation solutions such as Puppet have been leaders in this space and have successfully migrated applications from conventional development practices. At the same time, the challenges that organisations have been facing from external threats has been growing exponentially. The challenge is to enhance proven security best practices to be adopted to the agility of the application development lifecycle. Barracuda Web Application Firewall (WAF) has been a long-standing cloud enabled security solution for application security needs. [Click here to learn more about the Barracuda Web Application Firewall](https://campus.barracuda.com/product/webapplicationfirewall/) 

![alt](https://www.barracuda.com/assets/img/sections/programs/azure/img_app-security_diagram1.png)

## Deploy a Barracuda Web Application Firewall (WAF) with a test web server

### "Quickstart" Install - CFT deploys completely new VPC and subnets
#### Use this [template URL](https://barracuda-dev-days.s3-us-west-2.amazonaws.com/waf-new-vpc.json) when deploying the CloudFormation Stack.

### "Custom" Install - Choose existing VPC and subnet
#### Use this [template URL](https://barracuda-dev-days.s3-us-west-2.amazonaws.com/waf-with-existing-vpc.json) when deploying the CloudFormation Stack.

## Prerequisites
* AWS account with sufficient access to deploy virtual machines
* Key pair for the region into which you will deploy
* Must deploy in one of the US regions
** us-east-1 (N. Virginia)
** us-east-2 (Ohio)
** us-west-1 (N. California)
** us-west-2 (Oregon)

## Cost considerations
### These CFTs _will_ deploy resources that incur cost. Note that using PAYG vs. BYOL will simplify the installation process but has a significantly higher cost. A Barracuda representative or partner can assist with acquiring an evaluation license.

## Browser Recommendations
### The tasks in the lab have been tested with Edge, Firefox, and Chrome. However, it is likely that other browsers such as Safari and Opera will work. 
We recommend utilizing 2 browser windows:
1. Browser window 1 with 2 tabs:
    * AWS Console
    * Barracuda WAF UI
2. Browser window 2 with 1 or more tabs:
    * Incognito/Private Tab connected to web application



## Lab Instructions
### 
We recommend utilizing 2 browser windows:
1. Browser window 1 with 2 tabs:
    * AWS Console
    * Barracuda WAF UI
2. Browser window 2 with 1 or more tabs:
    * Incognito/private tab connected to web application
