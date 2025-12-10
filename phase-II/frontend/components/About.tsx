export default function About() {
  const features = [
    {
      icon: '⚡',
      title: 'Lightning Fast',
      description: 'Built with modern technology for optimal performance and speed.'
    },
    {
      icon: '🔒',
      title: 'Secure & Private',
      description: 'Your tasks are securely stored and accessible only to you.'
    },
    {
      icon: '📱',
      title: 'Responsive Design',
      description: 'Works perfectly on all devices from mobile to desktop.'
    }
  ];

  return (
    <section id="about" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-6">
            Why Choose Our Todo App?
          </h2>
          <p className="text-lg text-white/80 max-w-3xl mx-auto">
            Our todo application is designed to help you organize your daily activities with ease.
            With a focus on simplicity, security, and performance, we provide the perfect solution
            for managing your tasks efficiently.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white/5 backdrop-blur-md rounded-xl p-8 border border-white/10 hover:border-red-500/50 transition-all duration-300 transform hover:scale-105"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
              <p className="text-white/70">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}