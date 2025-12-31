import { prisma } from '~/lib/prisma/client'

export default defineEventHandler(async (event) => {
  try {
    // サンプルユーザーを取得（データがない場合は空配列）
    const users = await prisma.user.findMany({
      take: 10,
      orderBy: {
        createdAt: 'desc'
      }
    })
    
    return { users }
  } catch (error) {
    console.error('Database error:', error)
    return { users: [], error: 'データベース接続エラー' }
  }
})
