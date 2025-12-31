import { gql } from '@apollo/client';

export const GET_USERS = gql`
  query GetUsers {
    users {
      id
      email
      username
      createdAt
      posts {
        id
        title
        published
      }
    }
  }
`;

export const GET_USER = gql`
  query GetUser($id: String!) {
    user(id: $id) {
      id
      email
      username
      createdAt
      posts {
        id
        title
        content
        published
        createdAt
      }
    }
  }
`;

export const CREATE_USER = gql`
  mutation CreateUser($email: String!, $username: String!, $password: String!) {
    createUser(email: $email, username: $username, password: $password) {
      id
      email
      username
      createdAt
    }
  }
`;

export const GET_POSTS = gql`
  query GetPosts {
    posts {
      id
      title
      content
      published
      createdAt
      author {
        id
        username
      }
    }
  }
`;

export const CREATE_POST = gql`
  mutation CreatePost($title: String!, $content: String, $authorId: String!) {
    createPost(title: $title, content: $content, authorId: $authorId) {
      id
      title
      content
      published
      createdAt
    }
  }
`;
