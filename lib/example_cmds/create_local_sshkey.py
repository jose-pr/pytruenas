"""
Create a local ssh keypair for the host and add it to root authorizedkeys
"""

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs
from logging import Logger
import asyncssh as _ssh


def run(client: TrueNASClient, args: PyTrueNASArgs, logger: Logger):

    logger.info(f"Getting hostname from network configuration from {client._api.host}")
    netconfig: dict[str, str] = client.api.network.configuration.config()
    hostname: str = netconfig["hostname"]

    keypair_name = hostname.upper()

    logger.info(f"Get the current if any SSH Key Pair named: {keypair_name}")
    keypair = client.api.keychaincredential._get(type="SSH_KEY_PAIR", name=keypair_name)
    if not keypair:
        logger.info(
            f"Generating a SSH Key Pair as it currently doesnt exists"
        )

        private_key = client.api.keychaincredential.generate_ssh_key_pair()[
            "private_key"
        ]
    else:
        private_key = keypair["attributes"]["private_key"]

    pubkey = _ssh.import_private_key(private_key).export_public_key().decode().strip()

    logger.info(f"Upsert the current if any SSH Key Pair named")
    keypair = client.api.keychaincredential._upsert(
        ("name", "!type"),
        (lambda x, id, result: logger.info(f"Action taken {x}, id of keypair: {id}")),
        type="SSH_KEY_PAIR",
        name=keypair_name,
        attributes={"private_key": private_key, "public_key": pubkey},
    )
    root = client.api.user._get(username='root') or {}
    authkeys = (root.get("sshpubkey") or '').splitlines()
    if pubkey not in authkeys:
        authkeys.append(pubkey)
        logger.info(f"Adding key to {root['username']}")
        client.api.user._update(root['id'], sshpubkey='\n'.join(authkeys))
    else:
        logger.info(f"User {root['username']} already has the key in its authorizedkeys")


    print(private_key)
