interface ProfileModel {
  name: string;
  age: number;
  hobbies?: string[]; // オプショナル
}

const Profile = ({ name, age, hobbies }: ProfileModel) => {
  return (
    <div>
      <hr />
      <div>Name: {name}</div>
      <div>Age: {age}</div>
      <div>
        <div>Hobby:</div>
        {
          hobbies &&
          <ul>
          {hobbies.map((hobby) => (
            /* リストにはkeyを設定することを忘れないように！ */
            <li key={hobby}>{hobby}</li>
          ))}
        </ul>
        }
      </div>
    </div>
  );
};

export default Profile;
