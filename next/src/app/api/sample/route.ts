// app/api/example/route.ts

import { NextRequest, NextResponse } from 'next/server';

export const GET = async (request: NextRequest): Promise<NextResponse> => {
  return NextResponse.json({ message: 'This is a GET request' });
};

export const POST = async (request: NextRequest): Promise<NextResponse> => {
  const body = await request.json();
  return NextResponse.json({ message: 'This is a POST request', data: body });
};

export const PUT = async (request: NextRequest): Promise<NextResponse> => {
  const body = await request.json();
  return NextResponse.json({ message: 'This is a PUT request', data: body });
};

export const PATCH = async (request: NextRequest): Promise<NextResponse> => {
  const body = await request.json();
  return NextResponse.json({ message: 'This is a PATCH request', data: body });
};

export const DELETE = async (request: NextRequest): Promise<NextResponse> => {
  return NextResponse.json({ message: 'This is a DELETE request' });
};

export const HEAD = async (request: NextRequest): Promise<Response> => {
  return new Response(null, { status: 200 });
};

export const OPTIONS = async (request: NextRequest): Promise<Response> => {
  return new Response(null, {
    status: 204,
    headers: {
      'Allow': 'GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS',
    },
  });
};

export const dynamic = 'force-dynamic';