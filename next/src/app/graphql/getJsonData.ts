interface AsyncCountResponse {
  data: any;
}

const jsonData = {
  name: 'Tom',
  age: 18
}

const getJsonData = (): Promise<AsyncCountResponse> => {
  return new Promise((resolve) =>
    setTimeout(() => resolve({ data: jsonData }), Math.random() * 3000)
  );
};

export { getJsonData };
