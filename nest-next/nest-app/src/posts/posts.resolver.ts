import { Resolver, Query, Mutation, Args } from '@nestjs/graphql';
import { PostsService } from './posts.service';
import { Post } from '../users/user.model';

@Resolver(() => Post)
export class PostsResolver {
  constructor(private postsService: PostsService) {}

  @Query(() => [Post], { name: 'posts' })
  async getPosts() {
    return this.postsService.findAll();
  }

  @Query(() => Post, { name: 'post', nullable: true })
  async getPost(@Args('id') id: string) {
    return this.postsService.findOne(id);
  }

  @Mutation(() => Post)
  async createPost(
    @Args('title') title: string,
    @Args('authorId') authorId: string,
    @Args('content', { nullable: true }) content?: string,
  ) {
    return this.postsService.create({ title, content, authorId });
  }

  @Mutation(() => Post)
  async updatePost(
    @Args('id') id: string,
    @Args('title', { nullable: true }) title?: string,
    @Args('content', { nullable: true }) content?: string,
    @Args('published', { nullable: true }) published?: boolean,
  ) {
    return this.postsService.update(id, { title, content, published });
  }

  @Mutation(() => Post)
  async deletePost(@Args('id') id: string) {
    return this.postsService.delete(id);
  }
}
