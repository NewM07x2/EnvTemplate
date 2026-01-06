import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// リクエストインターセプター（トークンを自動付与）
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// レスポンスインターセプター（エラーハンドリング）
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // トークン無効時の処理
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: async (email: string, username: string, password: string) => {
    const response = await api.post('/api/auth/register', {
      email,
      username,
      password,
    });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await api.post('/api/auth/login', { email, password });
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/api/auth/logout');
    localStorage.removeItem('access_token');
    return response.data;
  },
};

// Users API
export const usersApi = {
  getUsers: async () => {
    const response = await api.get('/api/users');
    return response.data;
  },

  getUser: async (userId: string) => {
    const response = await api.get(`/api/users/${userId}`);
    return response.data;
  },

  deleteUser: async (userId: string) => {
    const response = await api.delete(`/api/users/${userId}`);
    return response.data;
  },
};

// Posts API
export const postsApi = {
  getPosts: async (published?: boolean) => {
    const response = await api.get('/api/posts', {
      params: { published },
    });
    return response.data;
  },

  getPost: async (postId: string) => {
    const response = await api.get(`/api/posts/${postId}`);
    return response.data;
  },

  createPost: async (
    title: string,
    content: string,
    published: boolean,
    authorId: string
  ) => {
    const response = await api.post('/api/posts', {
      title,
      content,
      published,
      author_id: authorId,
    });
    return response.data;
  },

  updatePost: async (
    postId: string,
    title: string,
    content: string,
    published: boolean
  ) => {
    const response = await api.put(`/api/posts/${postId}`, {
      title,
      content,
      published,
    });
    return response.data;
  },

  deletePost: async (postId: string) => {
    const response = await api.delete(`/api/posts/${postId}`);
    return response.data;
  },
};
