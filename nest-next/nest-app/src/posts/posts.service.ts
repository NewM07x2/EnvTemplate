import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class PostsService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.post.findMany({
      include: {
        author: true,
      },
    });
  }

  async findOne(id: string) {
    return this.prisma.post.findUnique({
      where: { id },
      include: {
        author: true,
      },
    });
  }

  async create(data: { title: string; content?: string; authorId: string }) {
    return this.prisma.post.create({
      data,
      include: {
        author: true,
      },
    });
  }

  async update(id: string, data: { title?: string; content?: string; published?: boolean }) {
    return this.prisma.post.update({
      where: { id },
      data,
      include: {
        author: true,
      },
    });
  }

  async delete(id: string) {
    return this.prisma.post.delete({
      where: { id },
    });
  }
}
