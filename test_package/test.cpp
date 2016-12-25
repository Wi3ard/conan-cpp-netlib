#define BOOST_NETWORK_ENABLE_HTTPS

#include <boost/network/protocol/http/client.hpp>
#include <iostream>

int main()
{
	using namespace boost::network;

	try
	{
		http::client::options options;
		options.always_verify_peer(false);

		http::client client(options);
		http::client::request request("https://httpbin.org/ip");
		request << header("Connection", "close");
		http::client::response response = client.get(request);
		std::cout << body(response) << std::endl;
	}
	catch (const std::exception& e)
	{
		std::cerr << e.what() << std::endl;
	}
	catch (...)
	{
		std::cerr << boost::current_exception_diagnostic_information() << std::endl;
	}

	return 0;
}
