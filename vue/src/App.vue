<template>
  <div class="app">
    <header class="app-header">
      <nav>
        <ul class="nav-list">
          <li><RouterLink to="/">ホーム</RouterLink></li>
          <li><RouterLink to="/graphql">GraphQL (CSR)</RouterLink></li>
          <li><RouterLink to="/prisma">Prisma (SSR)</RouterLink></li>
        </ul>
      </nav>
    </header>
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: #1a1a1a;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-list {
  list-style: none;
  display: flex;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-list a {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-list a:hover,
.nav-list a.router-link-active {
  color: #42b883;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
