from troposphere import Join, Ref, Template, GetAtt, Output, Parameter, Tags
from troposphere.ec2 import Subnet, RouteTable, Route, SubnetRouteTableAssociation, NatGateway, EIP

class SceptreRessource():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.igw_id = self.sceptre_user_data.pop("GatewayId")
        self.add_parameters()
        self.add_resource()
        self.add_outputs()

    def add_parameters(self):
        self.PublicSubnet = self.template.add_parameter(Parameter(
            "PublicSubnet",
            Default="10.0.1.0/24",
            Type="String",
        ))

        self.PrivateSubnet = self.template.add_parameter(Parameter(
            "PrivateSubnet",
            Default="10.0.10.0/24",
            Type="String",
        ))

        self.AvailabilityZone = self.template.add_parameter(Parameter(
            "AvailabilityZone",
            Default="eu-west-1a",
            Type="AWS::EC2::AvailabilityZone::Name",
        ))

    def add_resource(self):
        self.PublicRouteTable = self.template.add_resource(RouteTable(
            "PublicRouteTable",
            VpcId=self.sceptre_user_data.get("VpcId"),
            Tags=Tags(
                Application=Ref("AWS::StackName"),
                Network="Public",
                Environment=self.sceptre_user_data.get("Environment"),
                Name=Join("-", ["RT-PU", self.sceptre_user_data.get("Project")]),
            ),
        ))

        self.PubSubnet = self.template.add_resource(Subnet(
            "PubSubnet",
            Tags=Tags(
                Application=Ref("AWS::StackName"),
                Environment=self.sceptre_user_data.get("Environment"),
                Network="Public",
                Name=Join("-", ["NT-PU", self.sceptre_user_data.get("Project")]),
            ),
            VpcId=self.sceptre_user_data.get("VpcId"),
            CidrBlock=Ref(self.PublicSubnet),
            AvailabilityZone=Ref(self.AvailabilityZone),
            MapPublicIpOnLaunch=True,
        ))

        self.PriSubnet = self.template.add_resource(Subnet(
            "PriSubnet",
            Tags=Tags(
                Application=Ref("AWS::StackName"),
                Environment=self.sceptre_user_data.get("Environment"),
                Network="Private",
                Name=Join("-", ["NT-PR", self.sceptre_user_data.get("Project")]),
            ),
            VpcId=self.sceptre_user_data.get("VpcId"),
            CidrBlock=Ref(self.PrivateSubnet),
            AvailabilityZone=Ref(self.AvailabilityZone),
        ))

        self.PublicRoute = self.template.add_resource(Route(
            "PublicRoute",
            GatewayId=self.igw_id,
            DestinationCidrBlock="0.0.0.0/0",
            RouteTableId=Ref(self.PublicRouteTable),
        ))

        self.PrivateRouteTable = self.template.add_resource(RouteTable(
            "PrivateRouteTable",
            VpcId=self.sceptre_user_data.get("VpcId"),
            Tags=Tags(
                Application=Ref("AWS::StackName"),
                Environment=self.sceptre_user_data.get("Environment"),
                Network="Private",
                Name=Join("-", ["RT-PR", self.sceptre_user_data.get("Project")]),
            ),
        ))

        self.PubSubnetRTAssoc = self.template.add_resource(SubnetRouteTableAssociation(
            "PubSubnetRTAssoc",
            SubnetId=Ref(self.PubSubnet),
            RouteTableId=Ref(self.PublicRouteTable),
        ))

        self.PriSubnetRTAssoc = self.template.add_resource(SubnetRouteTableAssociation(
            "PriSubnetRTAssoc",
            SubnetId=Ref(self.PriSubnet),
            RouteTableId=Ref(self.PrivateRouteTable),
        ))

        self.nat_eip = self.template.add_resource(EIP(
            'NatEip',
            Domain="vpc",
            ))

        self.NatGateway = self.template.add_resource(NatGateway(
            "NatGateway",
            AllocationId=GetAtt(self.nat_eip, 'AllocationId'),
            SubnetId=Ref(self.PriSubnet),
            Tags=Tags(
                Application=Ref("AWS::StackName"),
                Environment=self.sceptre_user_data.get("Environment"),
                Name=Join("-", ["NAT-PR", self.sceptre_user_data.get("Project")]),
            ),
        ))

        self.NatRoute = self.template.add_resource(Route(
            'NatRoute',
            RouteTableId=Ref(self.PrivateRouteTable),
            DestinationCidrBlock='0.0.0.0/0',
            NatGatewayId=Ref(self.NatGateway),
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("PublicRouteTable", Value=Ref(self.PublicRouteTable)),
            Output("PrivateRouteTable", Value=Ref(self.PrivateRouteTable)),
            Output("PubSubnet", Value=Ref(self.PubSubnet)),
            Output("PriSubnet", Value=Ref(self.PriSubnet)),
            Output("NatGateway", Value=Ref(self.NatGateway)),
        ])

def sceptre_handler(sceptre_user_data):
    return SceptreRessource(sceptre_user_data).template.to_yaml()
