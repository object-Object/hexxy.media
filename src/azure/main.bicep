extension 'br:mcr.microsoft.com/bicep/extensions/microsoftgraph/v1.0:1.0.0'

import { projectInfoType } from 'project.bicep'

targetScope = 'subscription'

param projectInfos projectInfoType[]

param location string = deployment().location

param resourceGroupName string = 'hexxy.media'

param artifactsRoleName string = 'hexxy.media Artifacts Role'

param artifactsGroupName string = 'hexxy.media Artifacts Group'

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

module projects 'project.bicep' = [
  for info in projectInfos: {
    scope: resourceGroup
    params: {
      info: info
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
    relationships: [for i in range(0, length(projectInfos)): projects[i].outputs.identityId]
    relationshipSemantics: 'replace'
  }
}

output identities array = [
  for (info, i) in projectInfos: {
    name: '${info.githubUser}/${info.githubRepo}'
    clientId: projects[i].outputs.clientId
  }
]
