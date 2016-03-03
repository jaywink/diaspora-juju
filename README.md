**NOTE! HOX! ACHTUNG! I don't maintain this charm any more. You can find a maintained version [on Launchpad](https://code.launchpad.net/~joe/charms/trusty/diaspora/trunk).**

# Overview

diaspora\* social network server. See more about diaspora* here -
http://diasporafoundation.org

**Note! This version corresponds to diaspora* 0.5.99.x development version (ie the 0.6 dev branch). Not guaranteed to 
work with older or newer major versions.**

# Usage

## diaspora* service

To install diaspora*, you will need to know the hostname that will be used.
Think carefully before installing, as this cannot be changed after installation.

To set the hostname, you will need to create a configuration file. At minimum
it needs the host name setting, but you can configure other parts of the
charm at the same time.

Note! While the hostname can be set after the initial deploy command - the
application will not be fully configured until a hostname is provided, so it is
wise to create a configuration file for the initial deploy command.

To deploy (from the Juju Charm store, once this lands there):

    juju deploy --config=<path to config> diaspora
  
Until the charm is found in the charm store, deploy from a local repository. To
do this first create a path `charms/trusty` somewhere. Change to that path and
clone this repository. Create the config file and then:

    juju deploy --config=<path to config> --repository=<path to charms/>
    local:trusty/diaspora

Currently Apache and Redis are installed inside the diaspora* container though
this will possible change.

### Hostname after deploy

If you didn't or forgot to set hostname during the deploy command, make sure to
set it before adding a db relation! Do;

    juju set diaspora hostname="yourhostname.tld"

## Database

If you don't already have one, you also need to deploy a database. Here we are
currently restricting ourselves to PostgreSQL.

To deploy just a plain database, you can do as follows:

    juju deploy postgresql

Optionally add `--to=0` to the command to deploy it to the Juju state machine.

## Finish install

Once services are deployed, create a relation with the database:

    juju add-relation postgresql:db-admin diaspora:db

This will then trigger the actual building of the application - as it cannot be
fully completed without a database.

**Important!** Please note diaspora* takes a very long time to install, due to
the many Ruby gems that need to be pulled in. Depending on machine, this could
be from 5 to 30 minutes. Use `juju debug-log` to see the current progress. When
it is ready you will see `Starting diaspora* server` in the log as one of the
final lines.

## Expose service

After everything is installed, you can expose:

    juju expose diaspora

Note down the public address of the diaspora* service and check that it works.

    juju status

## Configuration

See `config.yaml` for all options ([link to file](https://github.com/jaywink/diaspora-juju/blob/master/config.yaml)).

The only required (and not changeable afterwards!) option is `hostname`.

### backup_*

A group of settings related to running backups of file uploads. See the [Juju Backup](https://code.launchpad.net/~jaywink/charms/trusty/jujubackup/trunk) charm and `config.yaml` for details. If the `jujubackup` charm is not installed, these settings have no effect.

## Upgrading diaspora*

To upgrade the diaspora* instance, you can use the following command:

    juju run --service=diaspora hooks/upgrade-diaspora

## Known Limitations and Issues

* Currently this charm supports only the PostgreSQL and Apache combination.
* This charm is currently for Ubuntu 14.04 (Trusty) targets only.
* Running several units at the same time has not been tested by the charm
  author.
* Removing the relation between PostgreSQL and Diaspora does not drop the
  database due to a timing issue with the hooks firing. If you need to
  reinstall the Diaspora service, please drop the `diaspora_production`
  database manually from the PostgreSQL admin console - or just destroy
  the whole PostgreSQL service.
  Issue tracked [here]
  (https://github.com/jaywink/diaspora-juju/issues/8).

# Contact Information

Discuss this charm in our Loomio [diaspora*
packaging](https://www.loomio.org/d/e7bKczxZ/install-diaspora-easily-with-a
-juju-charm-or-ppa) group.

## Charm Contact

Contact the charm author;

* diaspora*: https://iliketoast.net/u/jaywink / jaywink@iliketoast.net
* xmpp: jaywink@dukgo.com
* email: mail@jasonrobinson.me

Please file bugs on [GitHub](https://github.com/jaywink/diaspora-juju). Pull
requests also welcome!

This charm is also on [Launchpad](https://launchpad.net/diaspora-juju), code
will be synced there from GitHub.

# License

[GNU General Public License v3 (GPL-3)](https://tldrlegal.com/license/gnu-
[general-public-license-v3-%28gpl-3%29).

The author provides this charm as is and under no situation is responsible for
what it does or doesn't do.
