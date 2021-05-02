from aws_cdk import core
import aws_cdk.aws_codebuild as cb
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3 as s3


class InfraStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")
        account_id = core.Aws.ACCOUNT_ID
        PROJECT_NUMBER = 1

        # To Store Frontend App
        frontend_bucket = s3.Bucket(self, "frontend",
                                    access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                    bucket_name=account_id + '-' + env_name + '-frontend',
                                    public_read_access=True,
                                    removal_policy=core.RemovalPolicy.DESTROY,
                                    website_index_document='index.html'
                                    )

        bucket_name = frontend_bucket.bucket_name

        github_token = core.SecretValue.secrets_manager("dev/github-token", json_field='github-from-marsApp')

        cb.GitHubSourceCredentials(self, "CodeBuildGitHubCreds",
                                          access_token=github_token
                                          )

        git_hub_source = cb.Source.git_hub(
            owner="manrodri",
            repo="30miniProjects",
            webhook=True,
            webhook_filters=[
                cb.FilterGroup.in_event_of(cb.EventAction.PUSH).and_branch_is(
                    "master").and_file_path_is('js30Projects/')
            ]
        )

        codebuild_project = cb.Project(
            self,
            "cb-frontend",
            source=git_hub_source,
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_3_0,
                environment_variables={
                    'WEB_BUCKET_NAME': cb.BuildEnvironmentVariable(value=bucket_name),
                    'PROJECT_NUMBER': cb.BuildEnvironmentVariable(value=str(PROJECT_NUMBER))
                }
            ),
        )

        allow_object_actions = iam.PolicyStatement(resources=[f"arn:aws:s3:::{bucket_name}/*"],
                                               actions=["s3:*"])
        allow_bucket_actions = iam.PolicyStatement(
            resources=[f"arn:aws:s3:::{bucket_name}"],
            actions=['s3:*'],
        )
        codebuild_project.add_to_role_policy(allow_object_actions)
        codebuild_project.add_to_role_policy(allow_bucket_actions)

    # The code that defines your stack goes here
