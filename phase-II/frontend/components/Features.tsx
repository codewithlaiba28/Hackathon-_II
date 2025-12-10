export default function Features() {
  const features = [
    {
      icon: '📝',
      title: 'Add Tasks',
      description: 'Easily create new tasks with titles, descriptions, and due dates.',
      color: 'from-red-500 to-red-600'
    },
    {
      icon: '✏️',
      title: 'Update Tasks',
      description: 'Modify existing tasks with real-time updates and changes.',
      color: 'from-red-600 to-red-700'
    },
    {
      icon: '🗑️',
      title: 'Delete Tasks',
      description: 'Remove completed or unwanted tasks with a single click.',
      color: 'from-red-700 to-red-800'
    },
    {
      icon: '✅',
      title: 'Mark Complete',
      description: 'Track your progress by marking tasks as complete.',
      color: 'from-red-500 to-orange-600'
    },
    {
      icon: '👁️',
      title: 'View All Tasks',
      description: 'See all your tasks in a clean, organized interface.',
      color: 'from-gray-700 to-gray-800'
    },
    {
      icon: '🔐',
      title: 'Secure Tasks',
      description: 'All tasks are securely stored and accessible only to you.',
      color: 'from-red-800 to-black'
    }
  ];

  return (
    <section id="features" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-6">
            Powerful Features
          </h2>
          <p className="text-lg text-white/80 max-w-3xl mx-auto">
            Our todo application provides all the tools you need to stay organized and productive.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white/5 backdrop-blur-md rounded-xl p-8 border border-white/10 hover:border-red-500/50 transition-all duration-300 transform hover:scale-105"
            >
              <div className={`w-16 h-16 rounded-full bg-linear-to-r ${feature.color} flex items-center justify-center mb-6 mx-auto shadow-lg`}>
                <span className="text-2xl">{feature.icon}</span>
              </div>
              <h3 className="text-xl font-semibold text-white mb-3 text-center">{feature.title}</h3>
              <p className="text-white/70 text-center">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}