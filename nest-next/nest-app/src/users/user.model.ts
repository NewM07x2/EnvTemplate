import { ObjectType, Field, ID } from '@nestjs/graphql';

@ObjectType()
export class User {
  @Field(() => ID)
  id: string;

  @Field()
  email: string;

  @Field()
  username: string;

  @Field()
  createdAt: Date;

  @Field()
  updatedAt: Date;

  @Field(() => [Post], { nullable: true })
  posts?: Post[];
}

@ObjectType()
export class Post {
  @Field(() => ID)
  id: string;

  @Field()
  title: string;

  @Field({ nullable: true })
  content?: string;

  @Field()
  published: boolean;

  @Field()
  authorId: string;

  @Field(() => User)
  author: User;

  @Field()
  createdAt: Date;

  @Field()
  updatedAt: Date;
}
