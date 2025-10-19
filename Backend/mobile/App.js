import React, { useEffect, useState } from "react";
import { View, Text, FlatList, TextInput, Button, Image, TouchableOpacity } from "react-native";
import * as ImagePicker from "expo-image-picker";
import { fetchUsers, uploadPhoto } from "./src/api";

export default function App() {
  const [users, setUsers] = useState([]);
  const [image, setImage] = useState(null);
  const [caption, setCaption] = useState("");

  useEffect(() => {
    fetchUsers().then(setUsers).catch(console.error);
  }, []);

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });
    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", {
      uri: image,
      name: "photo.jpg",
      type: "image/jpeg",
    });
    formData.append("caption", caption);
    await uploadPhoto(formData);
    alert("Photo uploaded!");
  };

  return (
    <View style={{ flex: 1, padding: 20, backgroundColor: "#fff" }}>
      <Text style={{ fontSize: 24, fontWeight: "bold", marginBottom: 10 }}>Code-Red Mobile</Text>

      <FlatList
        data={users}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <Text>{item.username} — {item.email}</Text>
        )}
      />

      <TouchableOpacity onPress={pickImage} style={{ marginVertical: 20 }}>
        <Text style={{ color: "blue" }}>Select Photo</Text>
      </TouchableOpacity>

      {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}

      <TextInput
        value={caption}
        onChangeText={setCaption}
        placeholder="Caption"
        style={{
          borderWidth: 1,
          padding: 10,
          marginVertical: 10,
          borderRadius: 5,
        }}
      />

      <Button title="Upload Photo" onPress={handleUpload} />
    </View>
  );
}

