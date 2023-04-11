INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('lmob8usbx9otu597', 'ruby', 'Open a website, do a search',
'require ''mechanize''
require ''json''

# Function to get top 10 search results from DuckDuckGo
def get_search_results(query)
  # Initialize Mechanize agent
  agent = Mechanize.new

  # Send a GET request to DuckDuckGo with the query
  page = agent.get("https://duckduckgo.com/html/?q=#{query}")

  # Find the search results
  results = page.search(''.result'')

  # Extract the top 10 results'' title and URL
  top_results = results.take(10).map do |result|
    {
      title: result.at(''.result__title'').text.strip,
      url: result.at(''.result__url'')[''href'']
    }
  end

  # Return the results as a Ruby hash
  top_results
end

# Get user input from command line
query = ARGV[0]

# Get the top 10 search results
search_results = get_search_results(query)

# Print the results as proper JSON
puts JSON.pretty_generate({ \"r\": search_results})
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('h7oggnvtyxfmvps1', 'python', 'Generate an image with a text from the user',
'from PIL import Image, ImageDraw
import sys

# create a black background image
img = Image.new(''RGB'', (400, 400), color=''black'')

# create a draw object
draw = ImageDraw.Draw(img)

text = sys.argv[1] if len(sys.argv) > 1 else ''Hello world''

# get the size of the text
text_size = draw.textsize(text)

# calculate the position to center the text
x = (400 - text_size[0]) // 2
y = (400 - text_size[1]) // 2

# draw the text in red color
draw.text((x, y), text, fill=''red'')

# save the image as output.png
img.save(''output.png'')
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('v77aj50hy7922kb9', 'python', 'Save input data to redis',
'import json
import os
import sys

import redis


# Connect to Redis
redis_host = os.environ.get(''REDIS_HOST'', ''localhost'')
redis_client = redis.Redis(host=redis_host)


def save_param(param_value):
    redis_client.rpush(''params'', param_value)


def get_params():
    params = redis_client.lrange(''params'', 0, -1)
    params = [param.decode(''utf-8'') for param in params]
    return { ''params'': params }


if __name__ == ''__main__'':
    # Get user input data
    param_value = sys.argv[1]

    # Save param
    save_param(param_value)

    # Get and print all params
    params = get_params()
    print(json.dumps(params))
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('dk8jnu1b9ccf39o5', 'python', 'Read from redis',
'import json
import os
import sys

import redis


# Connect to Redis
redis_host = os.environ.get(''REDIS_HOST'', ''localhost'')
redis_client = redis.Redis(host=redis_host)


def save_param(param_value):
    redis_client.rpush(''params'', param_value)


def get_params():
    params = redis_client.lrange(''params'', 0, -1)
    params = [param.decode(''utf-8'') for param in params]
    return { ''params'': params }


if __name__ == ''__main__'':
    # Get user input data
    param_value = sys.argv[1]

    # Save param
    save_param(param_value)

    # Get and print all params
    params = get_params()
    print(json.dumps(params))
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('2tocc2qwbu6dfk5u', 'python', 'Generate graph from numbers provided in CSV',
'import csv
import os
import matplotlib.pyplot as plt

# Read numbers from a CSV file
def read_numbers_from_csv(file_path):
    numbers = []
    with open(file_path, ''r'') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            for number in row:
                try:
                    numbers.append(float(number))
                except ValueError:
                    print(f"Skipping non-numeric value: {number}")
    return numbers

# Plot numbers and save the plot to disk
def plot_and_save_numbers(numbers, output_path):
    plt.plot(numbers)
    plt.xlabel(''Index'')
    plt.ylabel(''Number'')
    plt.title(''Numbers Plot'')
    plt.savefig(output_path)

# Main function
def main():
    input_file_path = os.path.join(''/data'', ''numbers.csv'')
    output_file_path = os.path.join(''numbers_plot.png'')

    numbers = read_numbers_from_csv(input_file_path)
    plot_and_save_numbers(numbers, output_file_path)
    print(f"Plot saved to {output_file_path}")

if __name__ == ''__main__'':
    main()
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('gvp0amaq8jz52nkd', 'python', 'Download website and return links',
'import os
import sys
import json
import requests
from bs4 import BeautifulSoup

def get_top_stories():
    # Fetch the Hacker News page content
    response = requests.get(''https://news.ycombinator.com'')
    content = response.content

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(content, ''lxml'')

    # Find the top 10 story titles and store them in a list
    titles = []
    stories = soup.find_all(''span'', class_=''titleline'')
    for story in stories[:10]:
        title = story.find(''a'').text
        titles.append(title)

    return titles


top_stories_titles = get_top_stories()
print(json.dumps({''r'': top_stories_titles}, indent=2))
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('6do6tb92ml7e054o', 'node', 'Add caption to an image',
'/*
USE THOSE AS PARAMS ⬇️
https://www.asiamediajournal.com/wp-content/uploads/2022/11/Free-Download-Funny-Cat-PFP-300x300.jpg
Some_Text
⬆️
*/

// Import required modules
const axios = require(''axios'');
const Jimp = require(''jimp'');

// Function to download an image from a URL
async function downloadImage(url) {
      const response = await axios.get(url, { responseType: ''arraybuffer'' });
  return Buffer.from(response.data, ''binary'');
}

// Function to add a caption to an image
async function addCaptionToImage(imageUrl, captionText) {
      try {
        // Download the image
    const imageBuffer = await downloadImage(imageUrl);

    // Read the image using Jimp
    const image = await Jimp.read(imageBuffer);

    // Load the default font with 48px size
    const font = await Jimp.loadFont(Jimp.FONT_SANS_64_BLACK);

    // Add the caption text to the image
    image.print(font, 10, 10, captionText);

    // Save the image as output.png
    await image.writeAsync(''output.png'');

    console.log(''Caption added to the image and saved as output.png'');
  } catch (error) {
        console.log(''Error adding caption to the image:'', error.message);
  }
}

// Get the command line arguments
const args = process.argv.slice(2);

if (args.length < 2) {
      console.log(''Please provide an image URL and caption text as command line arguments.'');
} else {
      const imageUrl = args[0];
  const captionText = args[1];

  // Call the addCaptionToImage function with the provided arguments
  addCaptionToImage(imageUrl, captionText);
}

/*
USE THOSE AS PARAMS ⬇️
https://www.asiamediajournal.com/wp-content/uploads/2022/11/Free-Download-Funny-Cat-PFP-300x300.jpg
Some_Text
⬆️
*/
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('hhbj4pmr1870mf6a', 'node', 'Request a joke from jokes API and return',
'// Import the required modules
const axios = require(''axios'');

// Function to fetch a joke from the JokeAPI
async function fetchJoke() {
      try {
        // Fetch a joke from the JokeAPI using axios
    const response = await axios.get(''https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit'');

    // Get the joke data from the response
    const jokeData = response.data;

    // Check if the joke is a single-part joke or a two-part joke
    if (jokeData.type === ''single'') {
          // Print the single-part joke
      console.log(jokeData.joke);
    } else {
          // Print the two-part joke
      console.log(`${jokeData.setup}\
${jokeData.delivery}`);
    }
  } catch (error) {
        console.error(''Error fetching joke:'', error.message);
  }
}

// Fetch and print a joke
fetchJoke();
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('j3vd3ayr3zxnvdy0', 'kali', 'Scan ports with nmap',
'nmap -sV -p 80,443,22 example.com
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('zd6ulzzeie95yusa', 'kali', 'Search for vulnerabilities with nikto (rather slow, ~300 seconds)',
'nikto -h http://example.com -Tuning 1-2
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('i0doyn6v4jsm9vwu', 'kali', 'Bruteforce MD5 password with john the ripper',
'# Save the hash to a file
hash=''5f4dcc3b5aa765d61d8327deb882cf99''
echo "$hash" > hash.txt

# Run John the Ripper on the hash file using the default wordlist and suppress output
john --format=raw-md5 hash.txt > /dev/null 2>&1

# Get the cracked password from John the Ripper''s output and suppress output
cracked_password=$(john --show --format=raw-md5 hash.txt 2>/dev/null | grep -oP ''(?<=:).*'')

# Print the cracked password
echo "Cracked password: ''$cracked_password''"

# Cleanup
rm hash.txt
rm hash.txt.john.pot 2>/dev/null
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('4uv97vivibwwa6q1', 'cpp', 'Read data from redis',
'#include <iostream>
#include <hiredis/hiredis.h>
#include <nlohmann/json.hpp>
#include <fstream>

using json = nlohmann::json;

int main(int argc, char *argv[]) {
    // Connect to Redis
    redisContext *redis = redisConnect(getenv("REDIS_HOST"), 6379);
    if (redis == NULL || redis->err) {
            std::cerr << "Error connecting to Redis" << std::endl;
        return 1;
    }

    // Create JSON object and serialize it
    json data;
    data["name"] = "John";
    data["age"] = 30;
    std::string serialized_data = data.dump();

    // Save data to Redis
    redisReply *reply = (redisReply*) redisCommand(redis, "SET foo %s", serialized_data.c_str());
    if (reply == NULL) {
            std::cerr << "Error saving data to Redis" << std::endl;
        return 1;
    }
    freeReplyObject(reply);

    // Print output
    json output;
    output["message"] = "Data saved to Redis";
    std::cout << output.dump(4) << std::endl;

    // Disconnect from Redis
    redisFree(redis);

    return 0;
}
', datetime('now'));

INSERT INTO functions (slug, runtime, name, code, created_at) VALUES ('guv9a3dqg5v4zyhv', 'cpp', 'Calculate first 1000 Fibbonaci numbers with boost',
'#include <iostream>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>
#include <nlohmann/json.hpp>

using namespace std;
using namespace boost::multiprecision;
using json = nlohmann::json;

// Custom serializer for cpp_int
namespace nlohmann {
        template<>
    struct adl_serializer<cpp_int> {
            static void to_json(json& j, const cpp_int& num) {
                j = num.str();
        }

        static void from_json(const json& j, cpp_int& num) {
                num = cpp_int(j.get<std::string>());
        }
    };
}

int main() {
    cpp_int a = 0, b = 1, c;
    int n = 1000;

    // Create a vector to store the Fibonacci numbers
    vector<cpp_int> fib_numbers;

    // Add the first two Fibonacci numbers to the vector
    fib_numbers.push_back(a);
    fib_numbers.push_back(b);

    // Calculate and store the next n-2 Fibonacci numbers
    for (int i = 2; i < n; i++) {
            c = a + b;
        a = b;
        b = c;
        fib_numbers.push_back(c);
    }

    // Create a JSON object and add the Fibonacci numbers array
    json output;
    output["fib"] = fib_numbers;

    // Print the JSON object to stdout
    cout << output.dump() << endl;

    return 0;
}
', datetime('now'));
