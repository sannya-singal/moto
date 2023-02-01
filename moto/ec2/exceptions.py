from moto.core.exceptions import RESTError
from typing import List, Optional, Union


# EC2 has a custom root-tag - <Response> vs <ErrorResponse>
# `terraform destroy` will complain if the roottag is incorrect
# See https://docs.aws.amazon.com/AWSEC2/latest/APIReference/errors-overview.html#api-error-response
EC2_ERROR_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Errors>
    <Error>
      <Code>{{error_type}}</Code>
      <Message>{{message}}</Message>
    </Error>
  </Errors>
  <{{request_id_tag}}>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</{{request_id_tag}}>
</Response>
"""


class EC2ClientError(RESTError):
    code = 400
    # EC2 uses <RequestID> as tag name in the XML response
    request_id_tag_name = "RequestID"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("template", "custom_response")
        self.templates["custom_response"] = EC2_ERROR_RESPONSE
        super().__init__(*args, **kwargs)


class DefaultVpcAlreadyExists(EC2ClientError):
    def __init__(self):
        super().__init__(
            "DefaultVpcAlreadyExists",
            "A Default VPC already exists for this account in this region.",
        )


class DependencyViolationError(EC2ClientError):
    def __init__(self, message):
        super().__init__("DependencyViolation", message)


class MissingParameterError(EC2ClientError):
    def __init__(self, parameter):
        super().__init__(
            "MissingParameter",
            f"The request must contain the parameter {parameter}",
        )


class InvalidDHCPOptionsIdError(EC2ClientError):
    def __init__(self, dhcp_options_id):
        super().__init__(
            "InvalidDhcpOptionID.NotFound",
            f"DhcpOptionID {dhcp_options_id} does not exist.",
        )


class InvalidRequest(EC2ClientError):
    def __init__(self):
        super().__init__("InvalidRequest", "The request received was invalid")


class InvalidParameterCombination(EC2ClientError):
    def __init__(self, msg):
        super().__init__("InvalidParameterCombination", msg)


class MalformedDHCPOptionsIdError(EC2ClientError):
    def __init__(self, dhcp_options_id):
        super().__init__(
            "InvalidDhcpOptionsId.Malformed",
            f'Invalid id: "{dhcp_options_id}" (expecting "dopt-...")',
        )


class InvalidKeyPairNameError(EC2ClientError):
    def __init__(self, key):
        super().__init__(
            "InvalidKeyPair.NotFound", f"The keypair '{key}' does not exist."
        )


class InvalidKeyPairDuplicateError(EC2ClientError):
    def __init__(self, key):
        super().__init__(
            "InvalidKeyPair.Duplicate", f"The keypair '{key}' already exists."
        )


class InvalidKeyPairFormatError(EC2ClientError):
    def __init__(self):
        super().__init__(
            "InvalidKeyPair.Format", "Key is not in valid OpenSSH public key format"
        )


class InvalidVPCIdError(EC2ClientError):
    def __init__(self, vpc_id: str):
        super().__init__("InvalidVpcID.NotFound", f"VpcID {vpc_id} does not exist.")


class InvalidSubnetIdError(EC2ClientError):
    def __init__(self, subnet_id):
        super().__init__(
            "InvalidSubnetID.NotFound", f"The subnet ID '{subnet_id}' does not exist"
        )


class InvalidFlowLogIdError(EC2ClientError):
    def __init__(self, count, flow_log_ids):
        super().__init__(
            "InvalidFlowLogId.NotFound",
            f"These flow log ids in the input list are not found: [TotalCount: {count}] {flow_log_ids}",
        )


class FlowLogAlreadyExists(EC2ClientError):
    def __init__(self):
        super().__init__(
            "FlowLogAlreadyExists",
            "Error. There is an existing Flow Log with the same configuration and log destination.",
        )


class InvalidNetworkAclIdError(EC2ClientError):
    def __init__(self, network_acl_id):
        super().__init__(
            "InvalidNetworkAclID.NotFound",
            f"The network acl ID '{network_acl_id}' does not exist",
        )


class InvalidVpnGatewayIdError(EC2ClientError):
    def __init__(self, vpn_gw):
        super().__init__(
            "InvalidVpnGatewayID.NotFound",
            f"The virtual private gateway ID '{vpn_gw}' does not exist",
        )


class InvalidVpnGatewayAttachmentError(EC2ClientError):
    def __init__(self, vpn_gw, vpc_id):
        super().__init__(
            "InvalidVpnGatewayAttachment.NotFound",
            f"The attachment with vpn gateway ID '{vpn_gw}' and vpc ID '{vpc_id}' does not exist",
        )


class InvalidVpnConnectionIdError(EC2ClientError):
    def __init__(self, network_acl_id):
        super().__init__(
            "InvalidVpnConnectionID.NotFound",
            f"The vpnConnection ID '{network_acl_id}' does not exist",
        )


class InvalidCustomerGatewayIdError(EC2ClientError):
    def __init__(self, customer_gateway_id: str):
        super().__init__(
            "InvalidCustomerGatewayID.NotFound",
            f"The customer gateway ID '{customer_gateway_id}' does not exist",
        )


class InvalidNetworkInterfaceIdError(EC2ClientError):
    def __init__(self, eni_id):
        super().__init__(
            "InvalidNetworkInterfaceID.NotFound",
            f"The network interface ID '{eni_id}' does not exist",
        )


class InvalidNetworkAttachmentIdError(EC2ClientError):
    def __init__(self, attachment_id):
        super().__init__(
            "InvalidAttachmentID.NotFound",
            f"The network interface attachment ID '{attachment_id}' does not exist",
        )


class InvalidSecurityGroupDuplicateError(EC2ClientError):
    def __init__(self, name):
        super().__init__(
            "InvalidGroup.Duplicate", f"The security group '{name}' already exists"
        )


class InvalidSecurityGroupNotFoundError(EC2ClientError):
    def __init__(self, name):
        super().__init__(
            "InvalidGroup.NotFound",
            f"The security group '{name}' does not exist",
        )


class InvalidPermissionNotFoundError(EC2ClientError):
    def __init__(self):
        super().__init__(
            "InvalidPermission.NotFound",
            "The specified rule does not exist in this security group",
        )


class InvalidPermissionDuplicateError(EC2ClientError):
    def __init__(self):
        super().__init__(
            "InvalidPermission.Duplicate", "The specified rule already exists"
        )


class InvalidRouteTableIdError(EC2ClientError):
    def __init__(self, route_table_id):
        super().__init__(
            "InvalidRouteTableID.NotFound",
            f"The routeTable ID '{route_table_id}' does not exist",
        )


class InvalidRouteError(EC2ClientError):
    def __init__(self, route_table_id, cidr):
        super().__init__(
            "InvalidRoute.NotFound",
            f"no route with destination-cidr-block {cidr} in route table {route_table_id}",
        )


class RouteAlreadyExistsError(EC2ClientError):
    def __init__(self, cidr):
        super().__init__(
            "RouteAlreadyExists", f"The route identified by {cidr} already exists"
        )


class InvalidInstanceIdError(EC2ClientError):
    def __init__(self, instance_id):
        if isinstance(instance_id, str):
            instance_id = [instance_id]
        if len(instance_id) > 1:
            msg = f"The instance IDs '{', '.join(instance_id)}' do not exist"
        else:
            msg = f"The instance ID '{instance_id[0]}' does not exist"
        super().__init__("InvalidInstanceID.NotFound", msg)


class InvalidInstanceTypeError(EC2ClientError):
    def __init__(self, instance_type, error_type="InvalidInstanceType.NotFound"):
        if isinstance(instance_type, str):
            msg = f"The instance type '{instance_type}' does not exist"
        else:
            msg = (
                f"The following supplied instance types do not exist: "
                f"[{', '.join(instance_type)}]"
            )
        super().__init__(error_type, msg)


class InvalidAMIIdError(EC2ClientError):
    def __init__(self, ami_id: Union[List[str], str]):
        super().__init__(
            "InvalidAMIID.NotFound",
            f"The image id '[{ami_id}]' does not exist",
        )


class UnvailableAMIIdError(EC2ClientError):
    def __init__(self, ami_id: str):
        super().__init__(
            "InvalidAMIID.Unavailable",
            f"The image id '[{ami_id}]' is no longer available",
        )


class InvalidAMIAttributeItemValueError(EC2ClientError):
    def __init__(self, attribute: str, value: str):
        super().__init__(
            "InvalidAMIAttributeItemValue",
            f'Invalid attribute item value "{value}" for {attribute} item type.',
        )


class MalformedAMIIdError(EC2ClientError):
    def __init__(self, ami_id: List[str]):
        super().__init__(
            "InvalidAMIID.Malformed", f'Invalid id: "{ami_id}" (expecting "ami-...")'
        )


class InvalidSnapshotIdError(EC2ClientError):
    def __init__(self):
        # Note: AWS returns empty message for this, as of 2014.08.22.
        super().__init__("InvalidSnapshot.NotFound", "")


class InvalidSnapshotInUse(EC2ClientError):
    def __init__(self, snapshot_id, ami_id):
        super().__init__(
            "InvalidSnapshot.InUse",
            f"The snapshot {snapshot_id} is currently in use by {ami_id}",
        )


class InvalidVolumeIdError(EC2ClientError):
    def __init__(self, volume_id):
        super().__init__(
            "InvalidVolume.NotFound", f"The volume '{volume_id}' does not exist."
        )


class InvalidVolumeAttachmentError(EC2ClientError):
    def __init__(self, volume_id, instance_id):
        super().__init__(
            "InvalidAttachment.NotFound",
            f"Volume {volume_id} can not be detached from {instance_id} because it is not attached",
        )


class InvalidVolumeDetachmentError(EC2ClientError):
    def __init__(self, volume_id, instance_id, device):
        super().__init__(
            "InvalidAttachment.NotFound",
            f"The volume {volume_id} is not attached to instance {instance_id} as device {device}",
        )


class VolumeInUseError(EC2ClientError):
    def __init__(self, volume_id, instance_id):
        super().__init__(
            "VolumeInUse",
            f"Volume {volume_id} is currently attached to {instance_id}",
        )


class InvalidAddressError(EC2ClientError):
    def __init__(self, ip):
        super().__init__("InvalidAddress.NotFound", f"Address '{ip}' not found.")


class LogDestinationNotFoundError(EC2ClientError):
    def __init__(self, bucket_name):
        super().__init__(
            "LogDestinationNotFoundException",
            f"LogDestination: '{bucket_name}' does not exist.",
        )


class InvalidAllocationIdError(EC2ClientError):
    def __init__(self, allocation_id):
        super().__init__(
            "InvalidAllocationID.NotFound",
            f"Allocation ID '{allocation_id}' not found.",
        )


class InvalidAssociationIdError(EC2ClientError):
    def __init__(self, association_id):
        super().__init__(
            "InvalidAssociationID.NotFound",
            f"Association ID '{association_id}' not found.",
        )


class InvalidVpcCidrBlockAssociationIdError(EC2ClientError):
    def __init__(self, association_id):
        super().__init__(
            "InvalidVpcCidrBlockAssociationIdError.NotFound",
            f"The vpc CIDR block association ID '{association_id}' does not exist",
        )


class InvalidVPCPeeringConnectionIdError(EC2ClientError):
    def __init__(self, vpc_peering_connection_id):
        super().__init__(
            "InvalidVpcPeeringConnectionId.NotFound",
            f"VpcPeeringConnectionID {vpc_peering_connection_id} does not exist.",
        )


class InvalidVPCPeeringConnectionStateTransitionError(EC2ClientError):
    def __init__(self, vpc_peering_connection_id):
        super().__init__(
            "InvalidStateTransition",
            f"VpcPeeringConnectionID {vpc_peering_connection_id} is not in the correct state for the request.",
        )


class InvalidServiceName(EC2ClientError):
    def __init__(self, service_name):
        super().__init__(
            "InvalidServiceName",
            f"The Vpc Endpoint Service '{service_name}' does not exist",
        )


class InvalidFilter(EC2ClientError):
    def __init__(self, filter_name, error_type="InvalidFilter"):
        super().__init__(error_type, f"The filter '{filter_name}' is invalid")


class InvalidNextToken(EC2ClientError):
    def __init__(self, next_token):
        super().__init__("InvalidNextToken", f"The token '{next_token}' is invalid")


class InvalidDependantParameterError(EC2ClientError):
    def __init__(self, dependant_parameter, parameter, parameter_value):
        super().__init__(
            "InvalidParameter",
            f"{dependant_parameter} can't be empty if {parameter} is {parameter_value}.",
        )


class InvalidDependantParameterTypeError(EC2ClientError):
    def __init__(self, dependant_parameter, parameter_value, parameter):
        super().__init__(
            "InvalidParameter",
            f"{dependant_parameter} type must be {parameter_value} if {parameter} is provided.",
        )


class InvalidAggregationIntervalParameterError(EC2ClientError):
    def __init__(self, parameter):
        super().__init__("InvalidParameter", f"Invalid {parameter}")


class InvalidParameterValueError(EC2ClientError):
    def __init__(self, parameter_value):
        super().__init__(
            "InvalidParameterValue",
            f"Value {parameter_value} is invalid for parameter.",
        )


class EmptyTagSpecError(EC2ClientError):
    def __init__(self):
        super().__init__(
            "InvalidParameterValue", "Tag specification must have at least one tag"
        )


class InvalidParameterValueErrorTagNull(EC2ClientError):
    def __init__(self):
        super().__init__(
            "InvalidParameterValue",
            "Tag value cannot be null. Use empty string instead.",
        )


class InvalidParameterValueErrorUnknownAttribute(EC2ClientError):
    def __init__(self, parameter_value):
        super().__init__(
            "InvalidParameterValue",
            f"Value ({parameter_value}) for parameter attribute is invalid. Unknown attribute.",
        )


class InvalidGatewayIDError(EC2ClientError):
    def __init__(self, gateway_id):
        super().__init__(
            "InvalidGatewayID.NotFound", f"The eigw ID '{gateway_id}' does not exist"
        )


class InvalidInternetGatewayIdError(EC2ClientError):
    def __init__(self, internet_gateway_id):
        super().__init__(
            "InvalidInternetGatewayID.NotFound",
            f"InternetGatewayID {internet_gateway_id} does not exist.",
        )


class GatewayNotAttachedError(EC2ClientError):
    def __init__(self, internet_gateway_id, vpc_id):
        super().__init__(
            "Gateway.NotAttached",
            f"InternetGatewayID {internet_gateway_id} is not attached to a VPC {vpc_id}.",
        )


class ResourceAlreadyAssociatedError(EC2ClientError):
    def __init__(self, resource_id):
        super().__init__(
            "Resource.AlreadyAssociated",
            f"Resource {resource_id} is already associated.",
        )


class TagLimitExceeded(EC2ClientError):
    def __init__(self):
        super().__init__(
            "TagLimitExceeded",
            "The maximum number of Tags for a resource has been reached.",
        )


class InvalidID(EC2ClientError):
    def __init__(self, resource_id):
        super().__init__("InvalidID", f"The ID '{resource_id}' is not valid")


class InvalidCIDRSubnetError(EC2ClientError):
    def __init__(self, cidr):
        super().__init__(
            "InvalidParameterValue", f"invalid CIDR subnet specification: {cidr}"
        )


class RulesPerSecurityGroupLimitExceededError(EC2ClientError):
    def __init__(self):
        super().__init__(
            "RulesPerSecurityGroupLimitExceeded",
            "The maximum number of rules per security group " "has been reached.",
        )


class MotoNotImplementedError(NotImplementedError):
    def __init__(self, blurb):
        super().__init__(
            f"{blurb} has not been implemented in Moto yet."
            " Feel free to open an issue at"
            " https://github.com/getmoto/moto/issues"
        )


class FilterNotImplementedError(MotoNotImplementedError):
    def __init__(self, filter_name: str, method_name: Optional[str]):
        super().__init__(f"The filter '{filter_name}' for {method_name}")


class CidrLimitExceeded(EC2ClientError):
    def __init__(self, vpc_id, max_cidr_limit):
        super().__init__(
            "CidrLimitExceeded",
            f"This network '{vpc_id}' has met its maximum number of allowed CIDRs: {max_cidr_limit}",
        )


class UnsupportedTenancy(EC2ClientError):
    def __init__(self, tenancy):
        super().__init__(
            "UnsupportedTenancy", f"The tenancy value {tenancy} is not supported."
        )


class OperationNotPermitted(EC2ClientError):
    def __init__(self, association_id):
        super().__init__(
            "OperationNotPermitted",
            f"The vpc CIDR block with association ID {association_id} may not be disassociated. It is the primary IPv4 CIDR block of the VPC",
        )


class InvalidAvailabilityZoneError(EC2ClientError):
    def __init__(self, availability_zone_value, valid_availability_zones):
        super().__init__(
            "InvalidParameterValue",
            f"Value ({availability_zone_value}) for parameter availabilityZone is invalid. "
            f"Subnets can currently only be created in the following availability zones: {valid_availability_zones}.",
        )


class AvailabilityZoneNotFromRegionError(EC2ClientError):
    def __init__(self, availability_zone_value):
        super().__init__(
            "InvalidParameterValue",
            f"Invalid Availability Zone ({availability_zone_value})",
        )


class NetworkAclEntryAlreadyExistsError(EC2ClientError):
    def __init__(self, rule_number):
        super().__init__(
            "NetworkAclEntryAlreadyExists",
            f"The network acl entry identified by {rule_number} already exists.",
        )


class InvalidSubnetRangeError(EC2ClientError):
    def __init__(self, cidr_block):
        super().__init__("InvalidSubnet.Range", f"The CIDR '{cidr_block}' is invalid.")


class InvalidCIDRBlockParameterError(EC2ClientError):
    def __init__(self, cidr_block):
        super().__init__(
            "InvalidParameterValue",
            f"Value ({cidr_block}) for parameter cidrBlock is invalid. This is not a valid CIDR block.",
        )


class InvalidDestinationCIDRBlockParameterError(EC2ClientError):
    def __init__(self, cidr_block):
        super().__init__(
            "InvalidParameterValue",
            f"Value ({cidr_block}) for parameter destinationCidrBlock is invalid. This is not a valid CIDR block.",
        )


class InvalidSubnetConflictError(EC2ClientError):
    def __init__(self, cidr_block):
        super().__init__(
            "InvalidSubnet.Conflict",
            f"The CIDR '{cidr_block}' conflicts with another subnet",
        )


class InvalidVPCRangeError(EC2ClientError):
    def __init__(self, cidr_block):
        super().__init__("InvalidVpc.Range", f"The CIDR '{cidr_block}' is invalid.")


# accept exception
class OperationNotPermitted2(EC2ClientError):
    def __init__(self, client_region, pcx_id, acceptor_region):
        super().__init__(
            "OperationNotPermitted",
            f"Incorrect region ({client_region}) specified for this request.VPC peering connection {pcx_id} must be accepted in region {acceptor_region}",
        )


# reject exception
class OperationNotPermitted3(EC2ClientError):
    def __init__(self, client_region, pcx_id, acceptor_region):
        super().__init__(
            "OperationNotPermitted",
            f"Incorrect region ({client_region}) specified for this request.VPC peering connection {pcx_id} must be accepted or rejected in region {acceptor_region}",
        )


class OperationNotPermitted4(EC2ClientError):
    def __init__(self, instance_id):
        super().__init__(
            "OperationNotPermitted",
            f"The instance '{instance_id}' may not be terminated. Modify its 'disableApiTermination' instance attribute and try again.",
        )


class InvalidLaunchTemplateNameAlreadyExistsError(EC2ClientError):
    def __init__(self):
        super().__init__(
            "InvalidLaunchTemplateName.AlreadyExistsException",
            "Launch template name already in use.",
        )


class InvalidLaunchTemplateNameNotFoundError(EC2ClientError):
    def __init__(self):
        super().__init__(
            "InvalidLaunchTemplateName.NotFoundException",
            "At least one of the launch templates specified in the request does not exist.",
        )


class InvalidLaunchTemplateNameNotFoundWithNameError(EC2ClientError):
    def __init__(self, name):
        super().__init__(
            "InvalidLaunchTemplateName.NotFoundException",
            f"The specified launch template, with template name {name}, does not exist",
        )


class InvalidParameterDependency(EC2ClientError):
    def __init__(self, param, param_needed):
        super().__init__(
            "InvalidParameterDependency",
            f"The parameter [{param}] requires the parameter {param_needed} to be set.",
        )


class IncorrectStateIamProfileAssociationError(EC2ClientError):
    def __init__(self, instance_id):
        super().__init__(
            "IncorrectState",
            f"There is an existing association for instance {instance_id}",
        )


class InvalidAssociationIDIamProfileAssociationError(EC2ClientError):
    def __init__(self, association_id):
        super().__init__(
            "InvalidAssociationID.NotFound",
            f"An invalid association-id of '{association_id}' was given",
        )


class InvalidVpcEndPointIdError(EC2ClientError):
    def __init__(self, vpc_end_point_id):
        super().__init__(
            "InvalidVpcEndpointId.NotFound",
            f"The VpcEndPoint ID '{vpc_end_point_id}' does not exist",
        )


class InvalidTaggableResourceType(EC2ClientError):
    def __init__(self, resource_type: str):
        super().__init__(
            "InvalidParameterValue",
            f"'{resource_type}' is not a valid taggable resource type for this operation.",
        )


class GenericInvalidParameterValueError(EC2ClientError):
    def __init__(self, attribute, value):
        super().__init__(
            "InvalidParameterValue",
            f"invalid value for parameter {attribute}: {value}",
        )


class InvalidSubnetCidrBlockAssociationID(EC2ClientError):
    def __init__(self, association_id):
        super().__init__(
            "InvalidSubnetCidrBlockAssociationID.NotFound",
            f"The subnet CIDR block with association ID '{association_id}' does not exist",
        )


class InvalidCarrierGatewayID(EC2ClientError):
    def __init__(self, carrier_gateway_id: str):
        super().__init__(
            "InvalidCarrierGatewayID.NotFound",
            f"The CarrierGateway ID '{carrier_gateway_id}' does not exist",
        )


class NoLoadBalancersProvided(EC2ClientError):
    def __init__(self):
        super().__init__(
            "InvalidParameter",
            "exactly one of network_load_balancer_arn or gateway_load_balancer_arn is a required member",
        )


class UnknownVpcEndpointService(EC2ClientError):
    def __init__(self, service_id):
        super().__init__(
            "InvalidVpcEndpointServiceId.NotFound",
            f"The VpcEndpointService Id '{service_id}' does not exist",
        )
