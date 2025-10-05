targetScope = 'resourceGroup'

@export()
type projectType = {
  repository: string
  environment: string
}

param username string

param projects projectType[]

param roleDefinitionId string

param location string = resourceGroup().location

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  name: 'hexxy-media-artifacts-${replace(username, '.', '-')}'
  location: location

  @batchSize(1)
  resource githubActionsCredentials 'federatedIdentityCredentials' = [
    for project in projects: {
      name: 'GitHubActions-${project.repository}-${project.environment}'
      properties: {
        audiences: ['api://AzureADTokenExchange']
        issuer: 'https://token.actions.githubusercontent.com'
        subject: 'repo:${username}/${project.repository}:environment:${project.environment}'
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

output principalId string = identity.properties.principalId
