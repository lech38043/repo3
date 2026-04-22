Steps to deploy infrastructure from your code.

0. !! IMPORTANT !!
File '.gitignore' need contains lines listed below:
    
    -- # LA IaaC exclude
    .terraform/
    .local_secrets/
    *.tfstate
    *.tfstate.backup
    *.lock.hcl
    *.auto.tfvars

1. Install Azure CLI and Terraform in your system.

2. Add 'az' and 'terraform' do %PATH, windows powershell example:

	[Environment]::SetEnvironmentVariable(
	"PATH",
	$env:PATH + ";C:\Terraform;C:\Program Files (x86)\Microsoft DKs\Azure\CLI2\wbin",
	"User")

3. In your local repository main directory make file 'secrets.auto.tfvars' and fill it with (wariables started with @ repleca by real data, first line is placed olny for order - must be existing in github secrets - and commented in 'secrets.auto.tfvars', serwer_name must be unique, therefore it's combined by addind 'sqlserver'+'${suffix}'+'database.windows.net'):

	-- # sql_serwer        = "@SERWER_NAME"
	sql_database        = "@DB_NAME"	
	sql_admin_login     = "@DB_USER_NAME"   
	sql_admin_password  = "@DB_USER_PASSWORD"

4. In the remote repository (github → settings → secrets and variables → actions), add the same data with the same names as in the previous step (this is necessary for the github action to properly populate the database with task data).

5. Before you deploy infrastructure, you need to login into azure environment by entering in your terminal:
    az login -> and login into your azure account in pupop window.

6. Now you can init terraform by entering in terminal command:
    terraform init -> this will download all neccesary proiders for terraform code.

7. Next deploy infrastructure by entering in terminal command:
    terraform apply -> and confirm entering 'yes'.

8. When azure infrastructure was deployed, you need to make commit in your repo and enter command:
    git push -> this start github actions saved in .github/workflows and as a result fill new database with data.
!! IMPORTANT !!
git cannot replace LF (unix type) to CRLF (windows) in '.github\worflows\*' when pushing files to remote repository for proper operation of github actions runner.

9. When your work was end, for saving money you can destroy whole resource group by enterning in yput terminal command:
    terraform destroy -> and confim entering 'yes'.

10. Next time, when you want to deploy infrastructure and suuply them using github actions you need only to follow steps 5,7 and 8.


