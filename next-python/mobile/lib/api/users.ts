import apiClient from './client';

export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
}

export const userApi = {
  // 全ユーザー取得
  getUsers: async (): Promise<User[]> => {
    const response = await apiClient.get<{ users: User[] }>('/api/users');
    return response.data.users;
  },

  // 特定ユーザー取得
  getUser: async (id: string): Promise<User> => {
    const response = await apiClient.get<{ user: User }>(`/api/users/${id}`);
    return response.data.user;
  },

  // ユーザー作成
  createUser: async (data: { name: string; email: string }): Promise<User> => {
    const response = await apiClient.post<{ user: User }>('/api/users', data);
    return response.data.user;
  },

  // ユーザー更新
  updateUser: async (id: string, data: Partial<User>): Promise<User> => {
    const response = await apiClient.put<{ user: User }>(
      `/api/users/${id}`,
      data
    );
    return response.data.user;
  },

  // ユーザー削除
  deleteUser: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/users/${id}`);
  },
};
