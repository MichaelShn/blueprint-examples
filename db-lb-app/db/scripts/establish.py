from cloudify import ctx

if __name__ == '__main__':

    ctx.logger.info('Gather cluster data.')

    mariadb_props = ctx.source.instance.runtime_properties
    cluster_props = ctx.target.instance.runtime_properties
    ctx.logger.info('MariaDB Props: {0}'.format(mariadb_props))
    ctx.logger.info('Cluster Props: {0}'.format(cluster_props))

    groups = mariadb_props.get(
        'sources', {}).get('all', {}).get('children', {})

    if 'cluster_members' not in cluster_props:
        cluster_props['cluster_members'] = []

    for group_name, group in groups.items():
        if group_name == 'galera_cluster':
            ctx.logger.info('Group hosts: {0}'.format(group['hosts']))
            for hostname, host in group['hosts'].items():
                cluster_props['cluster_members'].append(
                    {
                        'name': hostname,
                        'address': host['ansible_host']
                    }
                )
    ctx.target.instance.runtime_properties['cluster_members'] = \
        cluster_props['cluster_members']

    ctx.logger.info('Finished gathering cluster data.')
