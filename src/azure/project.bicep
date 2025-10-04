targetScope = 'resourceGroup'

@export()
type projectInfoType = {
  githubUser: string
  githubRepo: string
  githubEnvironments: string[]
}

param info projectInfoType

param roleDefinitionId string

param location string = resourceGroup().location

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  name: replace('hexxy-media-artifacts-${info.githubUser}-${info.githubRepo}', '.', '-')
  location: location

  resource githubActionsCredentials 'federatedIdentityCredentials' = [
    for environment in info.githubEnvironments: {
      name: 'GitHubActions-${environment}'
      properties: {
        audiences: ['api://AzureADTokenExchange']
        issuer: 'https://token.actions.githubusercontent.com'
        subject: 'repo:${info.githubUser}/${info.githubRepo}:environment:${environment}'
      }
    }
  ]
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, roleDefinitionId, identity.id)
  properties: {
    roleDefinitionId: roleDefinitionId
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

output clientId string = identity.properties.clientId

output identityId string = identity.id
