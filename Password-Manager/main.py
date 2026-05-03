import click

def create_user():
    click.echo("\nCreating New User...")
    username = click.prompt("Enter new username")
    password = click.prompt("Enter new master password", hide_input=True)
    
    #store password in auth.json
    #generate elgamal public and private key (module 1)
    
    #generate aes key from master password
    #initialize vault and encrypt is use aes key (module 2)
    #sign the vault (module 3)
    
    click.echo(f"User '{username}' created successfully!")
    

def login():
    click.echo("\nLogin...")
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)
    # Add authentication logic here with auth.json
    
    #verify and decrypt
    #display the functionalities he can do with the vault
    #return to add_update_delete_view_4
    click.echo(f"Welcome back, {username}!")
    
def add_update_delete_view_4():
    ...
    #make the chanfe
    #encrtpy and sign the vault
    #return to login
    
    
    
def export():
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
