# Oracle OCI - Instances flagged for reboot migration
# Version 1.0 03-December 2018
# Written by: radu.dobrinescu@oracle.com
#
# Instructions:
# - you need the OCI python API, this can be installed by running: pip install oci
# - you need the OCI CLI, this can be installed by running: pip install oci-cli
# - Make sure you have a user with an API key setup in the OCI Identity
# - Create a config file using the oci cli tool by running: oci setup config
# - In the script specify the config file to be used for running the report
# - You can specify any region in the config file, the script will query all enabled regions

import oci

configfile = "/home/opc/.oraclebmc/config"

config = oci.config.from_file(configfile)
compartment_id = config["tenancy"]

identity_client = oci.identity.IdentityClient(config)
response = identity_client.list_region_subscriptions(config["tenancy"])
regions = response.data


def reboot_migration_instances():
    # Get all instances which have the reboot migration flag set.
    structured_search = oci.resource_search.models.StructuredSearchDetails(query="query instance resources where timeMaintenanceRebootDue > 'Now'",
                                                                           type='Structured',
                                                                           matching_context_type=oci.resource_search.models.SearchDetails.MATCHING_CONTEXT_TYPE_NONE)
    instances = search_client.search_resources(structured_search)
    for instance in instances.data.items:
        print("{}, {}, {}".format(instance.display_name, instance.identifier, instance.availability_domain))

print("")
print("Instances flagged for maintenance reboot: Instance Name, OCID, Availability Domain")
print("==================================================================================")
for region in regions:
        config["region"] = region.region_name
        search_client = oci.resource_search.ResourceSearchClient(config)
        reboot_migration_instances()
