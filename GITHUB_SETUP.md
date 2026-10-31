# Publishing to GitHub

Replace `YOUR_USERNAME` and create an empty repository on GitHub before running these commands.

```powershell
cd "c:\Users\ADMIN\Desktop\data analysis project"
git init
git add .
git commit -m "Add retail sales end-to-end data analysis project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/retail-sales-data-analysis.git
git push -u origin main
```

Important: create the GitHub repository without adding a README, license, or `.gitignore`, otherwise the first push may require merging histories.
