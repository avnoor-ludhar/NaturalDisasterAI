const Post = ({ post }: any) => {
    return (
        <div className="w-[400px] h-fit bg-gray-200 rounded-xl shadow-md p-4">
            <p className="font-semibold text-lg mb-2">Disaster: {post.disaster}</p>
            <p className="text-gray-700 mb-1">City: {post.city}</p>
            <p className="text-gray-700 mb-1">Province: {post.province}</p>
            <p className="text-gray-700 mb-1">Content: {post.content}</p>
            <p className="text-gray-500 text-sm">Posted at: {post.curr_time}</p>
        </div>
    );
};

export default Post;
