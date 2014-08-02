# Overview

diaspora\* social network server. See more about diaspora* here -
http://diasporafoundation.org

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

## Database

If you don't already have one, you also need to deploy a database. Here we are
currently restricting ourselves to PostgreSQL.

To deploy just a plain database, you can do as follows:

    juju deploy postgresql

Optionally add `--to=0` to the command to deploy it to the Juju state machine.

### Database storage

*Totally optionally not-relating-to-diaspora section below*

If you are on OpenStack or EC2 and want to attach a volume to the database
automatically, `block-storage-broker` and `storage` to handle that part. It
makes sense to deploy block-storage-broker to machine 0 (the Juju state
machine).

Unfortunately, currently the `block-storage-broker` charm doesn't work for
`trusty` - but I pulled a branch together combining fixes from the `precise`
branch. To use that, you need
[Bazaar](https://help.ubuntu.com/14.04/serverguide/bazaar.html) installed, then
in a suitable working path:

    mkdir trusty
    bzr checkout lp:~jaywink/charms/trusty/block-storage-broker
    /fix-for-trusty trusty/block-storage-broker

Check out also a fixed version of `storage`:

    bzr checkout lp:~jaywink/charms/trusty/storage/fix-fstab-mount
    trusty/storage

Create a .yml config file [specifying the
necessary](https://jujucharms.com/~lazypower/trusty/block-storage-broker-0/?text
=block-storage-broker#configuration) authorization details, for example as
follows:

    block-storage-broker:
      default_volume_size: 10
      endpoint: (openstack/ec2 api endpoint)
      key: (openstack/ec2 api username/key)
      secret: (openstack/ec2 api secret)
      region: (region)
      tenant: (tenant)
    storage:
      provider: block-storage-broker
      volume_size: 10

Then;

    juju deploy --repository=<path to working dir> local:trusty/block-storage-
    broker --to=0 --config=<path to config file>
    juju deploy --repository=<path to working dir> local:trusty/storage
    --config=<path to config file>

Then, deploy the database:

    juju deploy postgresql
    juju add-relation postgresql storage
    juju add-relation storage block-storage-broker

In theory you should soon get a volume attached to the postgresql machine
automatically. If this does not happen, check `juju debug-log`.

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

### hostname

Pod hostname in the format `domain.tld`. Subdomains are allowed. This is
required and *cannot* be changed after installation.

Note! Subfolders are not supported by diaspora* at this moment.

### repository

Default: diaspora/diaspora

Repository to use. Does not normally need to be changed.

### branch

Default: master

Branch to use. Does not normally need to be changed.

### podname

Default: diaspora*

A name for the pod. The most difficult setting. Can be changed later.

### ssl_key

SSL private key for pod domain. See readme how to best use this configuration
value. Must be unencrypted.

### ssl_cert

SSL cert for pod domain. See readme how to best use this configuration value.

### ssl_snakebite

Default: True

If you don't set `ssl_key` and `ssl_cert`, by default the default snakebite
self-signed certifications will be used until a proper cert is set. Set this to
false once you transfer the cert manually to the server.

Note! diaspora\* requires a valid SSL certificate for federation. Running a
production real diaspora* pod using snakebite certs is **not** possible.

### statistics

Default: false

Enable statistics from the pod? This includes user and post counts. Statistics
will be exposed at /statistics.json

### enable_registrations

Default: true

Enable new users to create accounts.

### bitcoin_address

Bitcoin address for donations.

### facebook_app_id

Facebook app id for services integration.

### facebook_app_secret

Facebook app secret if ID given.

### twitter_key

Twitter key for services integration.

### twitter_secret

Twitter secret if key given.

### tumblr_key

Tumblr key for services integration.

### tumblr_secret

Tumblr secret if ID given.

### admin_account

Once created, set admin account username here.

### admin_email

Set pod administrator email here.

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

This charm is not officially supported by the [diaspora*
project](http://diasporafoundation.org).

Discuss this charm in our Loomio [diaspora*
packaging](https://www.loomio.org/d/e7bKczxZ/install-diaspora-easily-with-a
-juju-charm-or-ppa) group.

## Charm Contact

Contact the charm author;

* diaspora*: https://iliketoast.net/u/jaywink or jaywink@iliketoast.net
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
