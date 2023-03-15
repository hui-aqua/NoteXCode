# Git / Github


## The first time use 
### setting your git username and email
1. open a terminal in anywhere.
2. Type as:
    ``` shell
    git config --global user.name "yourName"
    git config --global user.email "yourEmail"
    ```
## Generat a ssh key and add to your accound

1. open a terminal in anywhere.
2. Type as:
    ``` shell
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
3. At the prompt, type a secure passphrase.

    **NOTE:** Must remember this passphras, you will need it later.
4. Adding your SSH key to the ssh-agent

    4.1 Start the ssh-agent in the background.      
    ``` shell
    eval "$(ssh-agent -s)"
    ```
    4.2 Add your SSH private key to the ssh-agent.
    ``` shell
    ssh-add ~/.ssh/id_ed25519
    ```
5. Add the SSH key to your account on GitHub.

    5.1 Select and copy the contents of the id_ed25519.pub file
    ``` shell
    cat ~/.ssh/id_ed25519.pub
    ```
    5.2 In the upper-right corner of any page, click your profile photo, then click *Settings*.
    
    5.3 Open In the "*Access*" section of the sidebar, click  *SSH and GPG keys*.
     Then Click *New SSH key*.
    
    5.4 Paste your public key into the "Key" field.