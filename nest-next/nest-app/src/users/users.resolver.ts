import { Resolver, Query, Mutation, Args } from '@nestjs/graphql';
import { UsersService } from './users.service';
import { User } from './user.model';

@Resolver(() => User)
export class UsersResolver {
  constructor(private usersService: UsersService) {}

  @Query(() => [User], { name: 'users' })
  async getUsers() {
    return this.usersService.findAll();
  }

  @Query(() => User, { name: 'user', nullable: true })
  async getUser(@Args('id') id: string) {
    return this.usersService.findOne(id);
  }

  @Mutation(() => User)
  async createUser(
    @Args('email') email: string,
    @Args('username') username: string,
    @Args('password') password: string,
  ) {
    return this.usersService.create({ email, username, password });
  }

  @Mutation(() => User)
  async updateUser(
    @Args('id') id: string,
    @Args('username', { nullable: true }) username?: string,
    @Args('email', { nullable: true }) email?: string,
  ) {
    return this.usersService.update(id, { username, email });
  }

  @Mutation(() => User)
  async deleteUser(@Args('id') id: string) {
    return this.usersService.delete(id);
  }
}
