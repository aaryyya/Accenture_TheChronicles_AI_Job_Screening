// src/components/FolderUpload.tsx
import React, { useRef, useState } from 'react';
import axios from 'axios';

const FolderUpload: React.FC = () => {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploadResponse, setUploadResponse] = useState<any>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    const filesArray = Array.from(files);
    setSelectedFiles(filesArray);

    const formData = new FormData();
    filesArray.forEach((file) => formData.append('files', file));

    try {
      setIsUploading(true);
      const res = await axios.post("http://localhost:8000/upload-cvfolder", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setUploadResponse(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white w-full flex flex-col items-center justify-center">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm border border-gray-100">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
          Upload CV Folder
        </h2>
        <div className="flex flex-col space-y-4">
          <button
            onClick={() => {
              if (inputRef.current) {
                inputRef.current.setAttribute("webkitdirectory", "true");
                inputRef.current.click();
              }
            }}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
          >
            Choose Folder
          </button>
          <input
            ref={inputRef}
            type="file"
            multiple
            onChange={handleFileChange}
            className="hidden"
          />
          {selectedFiles.length > 0 && (
            <div className="border border-gray-200 p-4 rounded-md w-full">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Files Selected: {selectedFiles.length}
              </h3>
              <ul className="max-h-40 overflow-y-auto">
                {selectedFiles.map((file, idx) => (
                  <li key={idx} className="text-gray-600 text-sm truncate">
                    {file.name}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {isUploading && (
            <div className="text-blue-500 text-center font-medium">Uploading...</div>
          )}
          {uploadResponse && (
            <div className="bg-green-50 border border-green-100 text-green-700 p-4 rounded-md w-full">
              <p className="font-semibold">{uploadResponse.message}</p>
              <p>
                {uploadResponse.file_count} file{uploadResponse.file_count > 1 && "s"} received.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FolderUpload;
