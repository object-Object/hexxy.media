using 'main.bicep'

param users = {
  FallingColors: [
    { repository: 'Hexal', environment: 'maven' }
    { repository: 'MoreIotas', environment: 'maven' }
    { repository: 'serialization-hooks', environment: 'maven' }
  ]
  'Real-Septicake': [
    { repository: 'HexThings', environment: 'maven' }
    { repository: 'HexxyPlanes', environment: 'maven' }
  ]
  Robotgiggle: [
    { repository: 'hierophantics', environment: 'maven' }
  ]
  TechTastic: [
    { repository: 'HexWeb', environment: 'publishing' }
  ]
}
