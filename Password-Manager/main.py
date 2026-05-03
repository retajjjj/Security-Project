import click
import os
from deffie_helman import main_transfer, main_import

def create_user():
    
    username = click.prompt("Enter new username")
    password = click.prompt("Enter new master password", hide_input=True)
    click.echo("Creating User")
    
    
    #generate elgamal public and private key (module 1)
    click.echo("Elgamal keys generated")
    
    #initialize vault and encrypt is use aes key (module 2)
    #sign the vault (module 3)
    click.echo("Vault created and encrypted and signed")
   
    
    
    folder_name = username
    #replace with vault.json , private.key , public.key
    file_name = "example.txt"

    folder_path = os.path.join("Users", folder_name)
    os.makedirs(folder_path, exist_ok=False)
    
    
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as f:
        f.write("This file was created inside the new folder!")

    click.echo(f"user initialized {username}")
    

def login():
    click.echo("\nLogin...")
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)
    # Add authentication logic here with auth.json
    
    #verify and decrypt
    click.echo("Vault verified and decrypted")

    #display the functionalities he can do with the vault
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
        add()
    elif choice == '2':
        view()
    elif choice == '3':
        update()
    elif choice == '4':
        delete()
    elif choice == '5':
        transfer()
    elif choice == '6':
        recieve()
    elif choice == '7':
        view()
   
def add():
    website = click.prompt("Website")
    username = click.prompt("Username")
    password = click.prompt("Password")
    
    #encrtpy and sign the vault
    #return to login
def view():
    ...
def update():
    ...
def delete():
    ...
def transfer():
    ...
def recieve():
    ...
    
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
