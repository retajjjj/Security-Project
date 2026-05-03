import click
import os
from deffie_helman import main_transfer, main_import
from module_1 import generate_keypair, load_private_key, load_public_key
from module_2 import createVault, loadVault, saveVault, add,retrieve, update,delete
from deffie_helman import main_import, main_transfer, get_vault_from_username


def create_user():
    
    username = click.prompt("Enter new username")
    password = click.prompt("Enter new master password", hide_input=True)
    click.echo("Creating User")
    
    vault_file_name = get_vault_from_username(username)
    
    if os.path.exists(vault_file_name):
        click.echo("Username already exists.")
        return
    

    #generate elgamal public and private key (module 1)
    generate_keypair(username, password)
    click.echo("Elgamal keys generated")
    
    #get private key
    xa = load_private_key(username, password)
    
    #sign the vault (module 3)
    createVault(password, vault_file_name, xa )
    click.echo("Vault created and encrypted and signed")

    click.echo(f"user initialized {username}")
    

def login():
    click.echo("\nLogin...")
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)
    
    
    #verify and decrypt
    
    vault_file_name = get_vault_from_username(username)
    
    
    try:
        ya = load_public_key(username)
        loadVault(password, vault_file_name, ya)
    except FileNotFoundError:
        click.echo("User not found.")
        return
    except Exception as e:
        click.echo(f"Login failed: {e}")
        return
    click.echo("Vault verified and decrypted")

    #display the functionalities he can do with the vault
    while True:
        click.echo("\nOptions")
        click.echo("1. Add credential")
        click.echo("2. View credential")
        click.echo("3. Update credential")
        click.echo("4. Delete credential")
        click.echo("5. Export vault")
        click.echo("6. Import vault")
        click.echo("7. Exit")
    
        choice = click.prompt("Please select an option", type=click.Choice(['1', '2', '3', '4', '5', '6', '7']), show_choices=False)

        if choice == '1':
            add_prompt(username, password)
        elif choice == '2':
            view_prompt(username, password)
        elif choice == '3':
            update_prompt(username, password)
        elif choice == '4':
            delete_prompt(username, password)
        elif choice == '5':
            transfer_prompt(username, password)
        elif choice == '6':
            recieve_prompt(username, password)
        elif choice == '7':
            break
   
def add_prompt(username, password):
    website = click.prompt("Website")
    username_data = click.prompt("Username")
    password_data = click.prompt("Password")
    
    xa = load_private_key(username, password)
    ya = load_public_key(username)
    vault_file_name = get_vault_from_username(username)
     
    try:
        add(password, vault_file_name, {"website": website, "username": username_data, "password": password_data}, xa, ya)
        click.echo("Credential added")
    except Exception as e:
        click.echo(f"Failed to add credential: {e}")
        
def view_prompt(username, password):
    
    ya = load_public_key(username)
    vault_file_name = get_vault_from_username(username)
    try:
        data = loadVault(password, vault_file_name, ya)
        credentials = data.get("credentials", [])
        if not credentials:
            click.echo("No credentials stored.")
            return

 
        index = click.prompt("Enter index you want to view its details", type=int)
        entry = retrieve(password, vault_file_name, index, ya)
        click.echo(f"\n  Website:  {entry['website']}")
        click.echo(f"  Username: {entry['username']}")
        click.echo(f"  Password: {entry['password']}")
    except Exception as e:
        click.echo(f"Error: {e}")
    
    
def update_prompt(username, password):
    xa = load_private_key(username, password)
    ya = load_public_key(username)
    vault_file_name = get_vault_from_username(username)
    
    try:
        data = loadVault(password, vault_file_name, ya)
        credentials = data.get("credentials", [])
        if not credentials:
            click.echo("No credentials stored.")
            return

        for i, cred in enumerate(credentials):
            click.echo(f"  [{i}] {cred['website']} — {cred['username']}")

        index   = click.prompt("Enter index to update", type=int)
        website_data = click.prompt("New website",  default=credentials[index]["website"])
        username_data   = click.prompt("New username", default=credentials[index]["username"])
        password_data     = click.prompt("New password")

        update(password, vault_file_name, {"website": website_data, "username": username_data, "password": password_data}, index, xa, ya)
        click.echo("Credential updated.")
    except Exception as e:
        click.echo(f"Error: {e}")
    
    
def delete_prompt(username, password):
    xa = load_private_key(username, password)
    ya = load_public_key(username)
    vault_file_name = get_vault_from_username(username)
    try:
        data = loadVault(password, vault_file_name, ya)
        credentials = data.get("credentials", [])
        if not credentials:
            click.echo("No credentials stored.")
            return
 
        for i, cred in enumerate(credentials):
            click.echo(f"  [{i}] {cred['website']} — {cred['username']}")
 
        index = click.prompt("Enter index to delete", type=int)
        delete(password, vault_file_name, index, xa, ya)
        click.echo("Credential deleted.")
    except Exception as e:
        click.echo(f"Error: {e}")
    
    
    
def transfer_prompt(username, password):
    hisusername = click.prompt("Enter the recipient's username")
    try:
        main_transfer(username, password, hisusername)
        click.echo("Vault transfered successfully.")
    except Exception as e:
        click.echo(f"Export failed: {e}")
        
        
def recieve_prompt(username, password):
    hisusername = click.prompt("Enter the sender's username")
    try:
        main_import(username, password, hisusername)
        click.echo("Vault recieved successfully.")
    except Exception as e:
        click.echo(f"Import failed: {e}")
    
    




@click.command()
def main():
    while True:
        click.echo("\nSecure Password Manager")
        click.echo("1. Create new user")
        click.echo("2. Login")
        click.echo("3. Exit")
        
        
        choice = click.prompt("Please select an option", type=click.Choice(['1', '2', '3']), show_choices=False)

        if choice == '1':
            create_user()
        elif choice == '2':
            login()
        elif choice == '3':
            click.echo("Exiting...")
            break

if __name__ == '__main__':
    main()
