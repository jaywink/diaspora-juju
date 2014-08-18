#!/usr/bin/env python

import shutil
import os
import stat
import sys

# add local lib directory to path to get access to charm helpers
sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], "lib"))
from charmhelpers.core import hookenv
from charmhelpers.fetch import apt_install


hooks = hookenv.Hooks()

def _set_backup_relation_config():
    """ """
    # Useful for debugging
    hookenv.relation_set(backup_sources=hookenv.config("backup_sources"))
    hookenv.relation_set(backup_destination=hookenv.config("backup_destination"))
    hookenv.relation_set(backup_schedule=hookenv.config("backup_schedule"))
    hookenv.relation_set(backup_ftp_password=hookenv.config("backup_ftp_password"))
    hookenv.relation_set(backup_passphrase=hookenv.config("backup_passphrase"))
    hookenv.relation_set(backup_backend=hookenv.config("backup_backend"))
    hookenv.relation_set(backup_aws_access_key_id=hookenv.config("backup_aws_access_key_id"))
    hookenv.relation_set(backup_aws_secret_access_key=hookenv.config("backup_aws_secret_access_key"))
    hookenv.relation_set(backup_swift_username=hookenv.config("backup_swift_username"))
    hookenv.relation_set(backup_swift_password=hookenv.config("backup_swift_password"))
    hookenv.relation_set(backup_swift_url=hookenv.config("backup_swift_url"))
    hookenv.relation_set(backup_strategy=hookenv.config("backup_strategy"))
    hookenv.relation_set(pre_backup_script_path=hookenv.config("pre_backup_script_path"))
    hookenv.relation_set(post_backup_script_path=hookenv.config("post_backup_script_path"))
    hookenv.relation_set(pre_restore_script_path=hookenv.config("pre_restore_script_path"))
    hookenv.relation_set(post_restore_script_path=hookenv.config("post_restore_script_path"))

@hooks.hook('backup-relation-joined')
def backup_relation_joined():
    """ """
    hookenv.log("backup_relation_joined")
    try:
        shutil.copyfile("files/pre_backup.sh", "/usr/local/sbin/pre_backup.sh")
        os.chmod("/usr/local/sbin/pre_backup.sh", stat.S_IEXEC)
        shutil.copyfile("files/post_backup.sh", "/usr/local/sbin/post_backup.sh")
        os.chmod("/usr/local/sbin/post_backup.sh", stat.S_IEXEC)
        shutil.copyfile("files/pre_restore.sh", "/usr/local/sbin/pre_restore.sh")
        os.chmod("/usr/local/sbin/pre_restore.sh", stat.S_IEXEC)
        shutil.copyfile("files/post_restore.sh", "/usr/local/sbin/post_restore.sh")
        os.chmod("/usr/local/sbin/post_restore.sh", stat.S_IEXEC)
    except:
        pass
    _set_backup_relation_config()

@hooks.hook('backup-relation-changed')
def backup_relation_changed():
    """ """
    hookenv.log("backup_relation_changed")
    _set_backup_relation_config()

@hooks.hook('backup-relation-broken')
def backup_relation_broken():
    """ """
    hookenv.log("backup_relation_broken")

if __name__ == "__main__":
    hooks.execute(sys.argv)
