extension 'br:mcr.microsoft.com/bicep/extensions/microsoftgraph/v1.0:1.0.0'

import { projectType } from 'user.bicep'

targetScope = 'subscription'

@description('A map of GitHub usernames to repositories/environments.')
param users { *: projectType[] }

param location string = deployment().location

param resourceGroupName string = 'hexxy.media'

param artifactsRoleName string = 'hexxy.media Artifacts Role'

param artifactsGroupName string = 'hexxy.media Artifacts Group'

var usersList = items(users)

resource resourceGroup 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: resourceGroupName
  location: location
}

resource artifactsRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(artifactsRoleName)
  properties: {
    roleName: artifactsRoleName
    type: 'customRole'
    assignableScopes: [
      resourceGroup.id
    ]
    permissions: []
  }
}

module userIdentities 'user.bicep' = [
  for user in usersList: {
    scope: resourceGroup
    params: {
      username: user.key
      projects: user.value
      roleDefinitionId: artifactsRole.id
    }
  }
]

resource artifactsGroup 'Microsoft.Graph/groups@v1.0' = {
  displayName: artifactsGroupName
  uniqueName: guid(artifactsGroupName)
  mailEnabled: false
  mailNickname: 'hexxy-media-artifacts'
  securityEnabled: true
  members: {
    relationships: [for i in range(0, length(usersList)): userIdentities[i].outputs.principalId]
    relationshipSemantics: 'replace'
  }
}

output clientIds array = [
  for (user, i) in usersList: {
    name: user.key
    clientId: userIdentities[i].outputs.clientId
  }
]
