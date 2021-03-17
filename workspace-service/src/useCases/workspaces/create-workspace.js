const { v4 } = require('uuid')
module.exports = (model) => async (workspacename) => {
  const uuid = v4()
  const repeated = await model.findAll({ where: { identifier: uuid } })
  if (repeated.length === 0) {
    const result = await model.create({ identifier: uuid, workspacename })
    return { uuid: uuid, workspaceId: result.workspaceId }
  }
  throw new Error('Workspace already exists')
}
